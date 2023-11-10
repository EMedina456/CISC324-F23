from typing import List
from collections import deque


class MemoryPage:
    def __init__(self, virtual_address, content):
        self.content = content
        self.virtual_address = virtual_address  # The virtual address of the page


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


class FIFOPageReplacementAlgorithm:
    def __init__(self, page_frame: PageFrame, page_table: PageTable,
                 tlb_cache: TLBCache):
        self.page_frame = page_frame
        self.page_table = page_table
        self.tlb_cache = tlb_cache
        self.queue = []  # FIFO Queue

    def try_allocate(self, new_page):
        # Check TLB cache first
        virtual_page = new_page.virtual_address
        # TODO: check if the page exists in the TLB cache (one line of code)
        tlb_hit = self.tlb_cache.lookup(virtual_page)
        # TODO: if the page exists in the TLB cache, return the physical frame (2 lines of code)
        if tlb_hit is not None:
            return tlb_hit

        # TODO: if the page exists in page table, update the TLB cache then return the physical frame allocated to the page (3 lines of code)
        if self.page_table.get_frame(virtual_page) is not None:
            self.tlb_cache.insert(virtual_page, self.page_table.get_frame(virtual_page))
            return self.page_table.get_frame(virtual_page)

        # TODO: If TLB miss, check if there's an available frame (one line of code)
        available_frame = self.page_frame.allocate_frame(new_page)

        # TODO: if there's an available frame, return the physical frame
        if available_frame != -1:
            # TODO: add the physical frame to the queue (one line of code)
            self.queue.append(available_frame)
            # TODO: update the TLB cache (one line of code)
            self.tlb_cache.insert(virtual_page, available_frame)
            return available_frame

        # TODO: if no frames available, return -1
        return -1

    def map_page(self, virtual_page, physical_frame) -> bool:
        return self.page_table.map_page(virtual_page, physical_frame)

    def replace_page(self, new_page):
        # Check TLB cache first
        virtual_page = new_page.virtual_address
        tlb_hit = self.tlb_cache.lookup(virtual_page)
        if tlb_hit is not None:
            self.queue.append(tlb_hit)
            return tlb_hit

        # TODO: Check if there's an available frame using a function implemented above (one line of code)
        available_frame = self.page_frame.allocate_frame(new_page)

        if available_frame != -1:
            self.queue.append(available_frame)
            return available_frame

        # TODO: If there's no available frame, replace the oldest page in the queue (Two lines of code). \
        # Hint: use the queue variable to access the oldest page in the queue and don't forget to add it again to the end of the queue
        frame_to_replace = self.queue.pop(0)
        self.queue.append(frame_to_replace)

        # TODO: Remove page table entry
        self.page_table.remove_page_table_entry(frame_to_replace)
        # Deallocate the old page and allocate the new page in its place (Two lines of code)
        self.page_frame.deallocate_frame(frame_to_replace)
        self.page_frame.allocate_frame(new_page)

        # TODO: Update TLB cache with the new mapping
        self.tlb_cache.insert(virtual_page, frame_to_replace)

        # TODO: Print a message for the page fault
        print(f"Page fault occurred. Page {new_page.content} loaded into frame {frame_to_replace}.")

        return frame_to_replace


class LRUPageReplacementAlgorithm:
    def __init__(self, page_frame: PageFrame, page_table: PageTable,
                 tlb_cache: TLBCache):
        self.page_frame = page_frame
        self.page_table = page_table
        self.tlb_cache = tlb_cache
        self.page_order = deque()

    def try_allocate(self, new_page):
        # Check TLB cache first
        virtual_page = new_page.virtual_address
        # TODO: check if the page exists in the TLB cache (one line of code)
        tlb_hit = self.tlb_cache.lookup(virtual_page)
        # TODO: if the page exists in the TLB cache, return the physical frame (2 lines of code)
        if tlb_hit is not None:
            return tlb_hit

        # TODO: if the page exists in page table, update the TLB cache then return the physical frame allocated to the page (3 lines of code)
        if self.page_table.get_frame(virtual_page) is not None:
            self.tlb_cache.insert(virtual_page, self.page_table.get_frame(virtual_page))
            return self.page_table.get_frame(virtual_page)

        # TODO: If TLB miss, check if there's an available frame (one line of code)
        available_frame = self.page_frame.allocate_frame(new_page)

        # TODO: if there's an available frame, return the physical frame
        if available_frame != -1:
            # TODO: add the physical frame to the queue to maintain th order (one line of code)
            self.page_order.append(available_frame)
            # TODO: update the TLB cache (one line of code)
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
            self.page_order.remove(tlb_hit)
            self.page_order.append(tlb_hit)
            return tlb_hit

        # TODO: Check if there's an available frame using a function implemented above (one line of code)
        available_frame = self.page_frame.allocate_frame(new_page)

        # TODO: if there's an available frame, return the physical frame
        if available_frame != -1:
            # TODO: add the physical frame to the queue to maintain th order (one line of code)
            self.page_order.append(available_frame)
            return available_frame

        # TODO: If there's no available frame, replace the least recently used page
        frame_to_replace = self.page_order.popleft()


        # TODO: Remove page table entry, use the frame_to_replace variable to access
        # the frame to be replaced (one line of code) and don't forget to update the queue 'page_order' (two lines of code)
        self.page_table.remove_page_table_entry(frame_to_replace)
        self.page_order.append(frame_to_replace)

        # TODO: Deallocate the old page and allocate the new page in its place (Two lines of code)
        self.page_frame.deallocate_frame(frame_to_replace)
        self.page_frame.allocate_frame(new_page)

        # TODO: Update TLB cache with the new mapping (one line of code)
        self.tlb_cache.insert(virtual_page, frame_to_replace)

        # Print a message for the page fault
        print(f"Page fault occurred. Page {new_page.content} loaded into frame {frame_to_replace}.")

        return frame_to_replace


def simulate_memory_management_lru(pages: List[MemoryPage], num_frames: int):
    # Initialize the page table, page frames, and TLB cache
    page_table = PageTable()
    page_frames = PageFrame(num_frames)
    tlb_cache = TLBCache(size=num_frames)  # Set the TLB cache size

    # Initialize the LRU page replacement algorithm
    lru_algorithm = LRUPageReplacementAlgorithm(page_frames, page_table,
                                                tlb_cache)

    page_faults = 0

    # Enumerate the pages and simulate the page replacement algorithm
    for page in pages:
        virtual_page = page.virtual_address
        physical_frame = lru_algorithm.try_allocate(page)

        if physical_frame != -1:
            page_status = lru_algorithm.map_page(virtual_page, physical_frame)
            if not page_status:
                print(f"Page fault occurred. Page {page.content} loaded into frame {physical_frame}.")
                page_faults += 1
        else:
            physical_frame = lru_algorithm.replace_page(
                MemoryPage(virtual_page, page.content))
            lru_algorithm.map_page(virtual_page, physical_frame)
            page_faults += 1

    # Return the number of page faults
    return page_faults


def simulate_memory_management_fifo(pages: List[MemoryPage], num_frames: int):
    # Initialize the page table, page frames, and TLB cache
    page_table = PageTable()
    page_frames = PageFrame(num_frames)
    tlb_cache = TLBCache(size=num_frames)  # Set the TLB cache size

    # Initialize the FIFO page replacement algorithm
    fifo_algorithm = FIFOPageReplacementAlgorithm(page_frames, page_table,tlb_cache)

    page_faults = 0
    # Enumerate the pages and simulate the page replacement algorithm
    for i, page in enumerate(pages):
        virtual_page = page.virtual_address
        physical_frame = fifo_algorithm.try_allocate(page)
        if physical_frame != -1:
            page_status = fifo_algorithm.map_page(virtual_page, physical_frame)
            if not page_status:
                print(f"Page fault occurred. Page {page.content} loaded into frame {physical_frame}.")
                page_faults += 1
        else:
            physical_frame = fifo_algorithm.replace_page(
                MemoryPage(virtual_page, page.content))
            fifo_algorithm.map_page(virtual_page, physical_frame)
            page_faults += 1

    # Return the number of page faults
    return page_faults


def main():
    # Sample input: A list of memory pages (could be program code or data)
    pages = [MemoryPage(virtual_address="page0", content="Page 0"),
             MemoryPage(virtual_address="page0", content="Page 0"),
             MemoryPage(virtual_address="page1", content="Page 1"),
             MemoryPage(virtual_address="page2", content="Page 2"),
             MemoryPage(virtual_address="page3", content="Page 3"),
             MemoryPage(virtual_address="page4", content="Page 4"),
             MemoryPage(virtual_address="page5", content="Page 5"),
             MemoryPage(virtual_address="page6", content="Page 6"),]

    num_frames = 2  # Number of available memory frames

    fifo_page_faults = simulate_memory_management_fifo(pages, num_frames)
    print("FIFO Total Page Faults:", fifo_page_faults)

    lru_page_faults = simulate_memory_management_lru(pages, num_frames)
    print("LRU Total Page Faults:", lru_page_faults)

if __name__ == "__main__":
    main()