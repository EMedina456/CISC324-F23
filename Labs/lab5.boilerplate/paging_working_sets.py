from typing import List
from collections import deque
from types import SimpleNamespace
import time


class MemoryPage:
    def __init__(self, virtual_address, content):
        self.content = content
        self.virtual_address = virtual_address  # The virtual address of the page
        self.last_referenced_time = time.time()  # Initialize the last referenced time


class PageTable:
    def __init__(self):
        self.table = {}  # a dictionary that maps a virtual address to a physical frame {virtual_page: physical_frame}

    # Returns true if the page exists in the page table and false otherwise
    def map_page(self, virtual_page, physical_frame) -> bool:
        # Check first if the virtual page is already mapped to a physical frame
        if virtual_page in self.table:
            # If it is, return true
            return True
        self.table[virtual_page] = physical_frame
        return False

    def get_frame(self, virtual_page):
        return self.table.get(virtual_page, None)

    def remove_page_table_entry(self, frame_index):
        for virtual_page, physical_frame in self.table.items():
            if physical_frame == frame_index:
                del self.table[virtual_page]
                return


class TLBCache:
    def __init__(self, size):
        self.cache = {}
        self.size = size
        self.queue = deque()

    def lookup(self, virtual_page):
        if virtual_page in self.cache:
            # TLB hit
            self.queue.remove(virtual_page)
            self.queue.append(virtual_page)
            return self.cache[virtual_page]
        else:
            # TLB miss
            return None

    def insert(self, virtual_page, physical_frame):
        if len(self.cache) >= self.size:
            # Remove the least recently used entry
            removed_page = self.queue.popleft()
            del self.cache[removed_page]

        self.cache[virtual_page] = physical_frame
        self.queue.append(virtual_page)


class PageFrame:
    def __init__(self, size: int):
        self.frames = [None] * size

    def allocate_frame(self, page_content: MemoryPage):
        for i, frame in enumerate(self.frames):
            if frame is None:
                self.frames[i] = page_content
                return i
        return -1  # No available frame

    def deallocate_frame(self, frame_index):
        self.frames[frame_index] = None


class WorkingSetPageReplacementAlgorithm:
    def __init__(self, page_frame: PageFrame, page_table: PageTable, tlb_cache: TLBCache, time_window: float):
        self.page_frame = page_frame
        self.page_table = page_table
        self.tlb_cache = tlb_cache
        self.time_window = time_window

    def try_allocate(self, new_page):
        # Check TLB cache first
        virtual_page = new_page.virtual_address
        tlb_hit = self.tlb_cache.lookup(virtual_page)
        if tlb_hit is not None:
            return tlb_hit

        # if the page exists in page table, update the TLB cache
        if self.page_table.get_frame(virtual_page) is not None:
            self.tlb_cache.insert(
                virtual_page, self.page_table.get_frame(virtual_page))
            return self.page_table.get_frame(virtual_page)

        # If TLB miss, check if there's an available frame
        available_frame = self.page_frame.allocate_frame(new_page)

        if available_frame != -1:
            self.tlb_cache.insert(virtual_page, available_frame)
            return available_frame

        return -1

    def map_page(self, virtual_page, physical_frame) -> bool:
        return self.page_table.map_page(virtual_page, physical_frame)

    def replace_page(self, new_page):
        # Check TLB cache first
        virtual_page = new_page.virtual_address
        tlb_hit = self.tlb_cache.lookup(virtual_page)
        if tlb_hit is not None:
            return tlb_hit

        # TODO: Check if there's an available frame using a function implemented above (one line of code)
        available_frame = None

        if available_frame != -1:
            return available_frame

        # If there's no available frame, replace the pages outside the working set
        # TODO: get current time using `time` package
        # Get the indecies of the frames outside the working set
        # TODO: you can do that with a loop that checks whether the last_referenced_time of the frame is within `self.time_window`
        working_set = None
        if not working_set:
            # TODO: If the working set is empty, get the index of the oldest page from page_frame.frames
            # Hint: you can get the oldest frame using a loop that checks the last_referenced_time of each frame
            frame_to_replace = None
        else:
            # TODO: Replace the oldest page outside the working set
            # Hint: it is similar to what you wrote at line 129 but you need to get the oldest page from the working_set
            frame_to_replace = None

        # TODO: Remove page table entry.

        # TODO: Deallocate the old page and allocate the new page in its place

        # TODO: Update TLB cache with the new mapping

        # Print a message for the page fault
        print(
            f"Page fault occurred. Page {new_page.content} loaded into frame {frame_to_replace}.")

        return frame_to_replace


class MultiprogrammingMemoryManager:
    def __init__(self, num_programs: int, program_pages: List[List[MemoryPage]], num_frames: int, time_window: float):
        self.num_programs = num_programs
        self.programs = []
        self.page_frame = PageFrame(num_frames)
        self.page_table = PageTable()
        self.tlb_cache = TLBCache(size=num_frames)

        for i in range(num_programs):
            working_set_algorithm = WorkingSetPageReplacementAlgorithm(
                self.page_frame, self.page_table, self.tlb_cache, time_window)
            self.programs.append((program_pages[i], working_set_algorithm))

    def simulate_memory_management(self):
        total_page_faults = 0

        for i in range(self.num_programs):
            program_page_faults = 0
            program_pages, working_set_algorithm = self.programs[i]

            for page in program_pages:
                virtual_page = page.virtual_address
                physical_frame = working_set_algorithm.try_allocate(page)

                if physical_frame != -1:
                    page_status = working_set_algorithm.map_page(
                        virtual_page, physical_frame)
                    if not page_status:
                        print(
                            f"Program {i + 1} Page fault occurred. Page {page.content} loaded into frame {physical_frame}.")
                        program_page_faults += 1
                else:
                    physical_frame = working_set_algorithm.replace_page(
                        MemoryPage(virtual_page, page.content))
                    working_set_algorithm.map_page(
                        virtual_page, physical_frame)
                    program_page_faults += 1

            print(f"Program {i + 1} Total Page Faults:", program_page_faults)
            total_page_faults += program_page_faults

        print("Total Page Faults for all programs:", total_page_faults)


def main():
    # Sample input: A list of memory pages for each program
    program1_pages = [
        MemoryPage(virtual_address="program1_page1",
                   content="Chrome - 1st tab"),
        MemoryPage(virtual_address="program1_page1",
                   content="Chrome - 1st tab"),
        MemoryPage(virtual_address="program1_page2",
                   content="Chrome - 2nd tab"),
        MemoryPage(virtual_address="program1_page1",
                   content="Chrome - 1st tab"),
        MemoryPage(virtual_address="program1_page3",
                   content="Chrome - 3rd tab"),
        MemoryPage(virtual_address="program1_page4",
                   content="Chrome - 4th tab"),
        # ... more pages for program 1
    ]

    program2_pages = [
        MemoryPage(virtual_address="program2_page1",
                   content="COD - 1st tab"),
        MemoryPage(virtual_address="program2_page1",
                   content="COD - 1st tab"),
        MemoryPage(virtual_address="program2_page2",
                   content="COD - 2nd tab"),
        MemoryPage(virtual_address="program2_page1",
                   content="COD - 1st tab"),
        MemoryPage(virtual_address="program2_page3",
                   content="COD - 3rd tab"),
        MemoryPage(virtual_address="program2_page4",
                   content="COD - 4th tab"),
        # ... more pages for program 2
    ]
    num_frames = 4  # Number of available memory frames shared among all programs
    time_window = 5.0  # Time window for the working set principle

    programs_pages = [program1_pages, program2_pages]

    # Create a MultiprogrammingMemoryManager with 2 programs
    multiprogram_manager = MultiprogrammingMemoryManager(
        num_programs=len(programs_pages),
        program_pages=programs_pages,
        num_frames=num_frames,
        time_window=time_window
    )

    # Simulate memory management for all programs
    multiprogram_manager.simulate_memory_management()


if __name__ == "__main__":
    main()
