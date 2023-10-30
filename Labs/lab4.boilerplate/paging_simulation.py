from collections import deque
from typing import List
class MemoryPage:
    def __init__(self, virtual_address, content):
        self.content = content
        self.virtual_address = virtual_address  # The virtual address of the page

class PageTable:
    def __init__(self):
        self.table = {} # a dictionary that maps a virtual address to a physical frame{virtual_page: physical_frame}

    def map_page(self, virtual_page, physical_frame):
        self.table[virtual_page] = physical_frame

    def get_frame(self, virtual_page):
        return self.table[virtual_page]
    
    def remove_page_table_entry(self, frame_index):
        for virtual_page, physical_frame in self.table.items():
            if physical_frame == frame_index:
                del self.table[virtual_page]
                return        

        
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
    def __init__(self, page_frame: PageFrame, page_table: PageTable):
        self.page_frame = page_frame
        self.page_table = page_table
        self.queue = []

    def try_allocate(self, new_page):
        # Check if there's an available frame
        available_frame = self.page_frame.allocate_frame(new_page)

        if available_frame != -1:
            self.queue.append(available_frame)
            return available_frame

        return -1
    
    def map_page(self, virtual_page, physical_frame):
        self.page_table.map_page(virtual_page, physical_frame)

    def replace_page(self, new_page):
        # TODO: Check if there's an available frame (can be implemented in four lines of code)
        

        # TODO: If there's no available frame, replace the oldest page (can be implemented in two lines of code)

        
        # TODO: Remove page table entry (can be implemented in one line of code)

        # TODO: Deallocate the old page and allocate the new page in its place (can be implemented in one lines of code)

        # TODO: Allocate frame for the new page (can be implemented in one line of code)

        # TODO: Print a message for the page fault
        print(f"Page fault occurred. Page {'NOT IMPLEMENTED'} loaded into frame {'NOT IMPLEMENTED'}.")
        # TODO: Return the frame that was replaced (can be implemented in one line of code)
        return None



class LRUPageReplacementAlgorithm:
    def __init__(self, page_frame: PageFrame, page_table: PageTable):
        self.page_frame = page_frame
        self.page_table = page_table
        self.page_order = deque() # a queue that keeps track of the order of pages that are used, but you can use whatever data structure you want

    def try_allocate(self, new_page):
        # Check if there's an available frame
        available_frame = self.page_frame.allocate_frame(new_page)

        if available_frame != -1:
            self.page_order.append(available_frame)
            return available_frame

        return -1

    def map_page(self, virtual_page, physical_frame):
        self.page_table.map_page(virtual_page, physical_frame)

    def replace_page(self, new_page):
        # TODO: remove 'pass' keyword before you start implementing the simulation
        pass
        # TODO: Check if there's an available frame

        # TODO: If there's no available frame, replace the least recently used page

        # TODO: Remove page table entry
        
        # TODO: Deallocate the old page and allocate the new page in its place
        
        # Print a message for the page fault
        print(f"Page fault occurred. Page {'NOT IMPLEMENTED'} loaded into frame {'NOT IMPLEMNETED'}.")

        return None

def simulate_memory_management_lru(pages: List[MemoryPage], num_frames: int):
    # Initialize the page table and page frames
    page_table = PageTable()
    page_frames = PageFrame(num_frames)

    # Initialize the LRU page replacement algorithm
    lru_algorithm = LRUPageReplacementAlgorithm(page_frames, page_table)

    page_faults = 0

    # Enumerate the pages and simulate the page replacement algorithm
    for page in pages:
        virtual_page = page.virtual_address
        physical_frame = lru_algorithm.try_allocate(page)

        if physical_frame != -1:
            lru_algorithm.map_page(virtual_page, physical_frame)
        else:
            physical_frame = lru_algorithm.replace_page(MemoryPage(virtual_page, page.content))
            lru_algorithm.map_page(virtual_page, physical_frame)
            page_faults += 1

    # Return the number of page faults
    return page_faults


def simulate_memory_management_fifo(pages: List[MemoryPage], num_frames: int):
    # Initialize the page table and page frames
    page_table = PageTable()
    page_frames = PageFrame(num_frames)

    # Initialize the FIFO page replacement algorithm
    fifo_algorithm = FIFOPageReplacementAlgorithm(page_frames, page_table)

    page_faults = 0
    # Enumerate the pages and simulate the page replacement algorithm
    for i, page in enumerate(pages):
        virtual_page = page.virtual_address
        physical_frame = fifo_algorithm.try_allocate(page)
        if physical_frame != -1:
            fifo_algorithm.map_page(virtual_page, physical_frame)
        else: 
            physical_frame = fifo_algorithm.replace_page(MemoryPage(virtual_page, page.content))
            fifo_algorithm.map_page(virtual_page, physical_frame)
            page_faults += 1

    # return the number of page faults
    return page_faults

def main():
    # Sample input: A list of memory pages (could be program code or data)
    pages = [MemoryPage(virtual_address="page0", content="Page 0"), 
             MemoryPage(virtual_address="page1", content="Page 1"), 
             MemoryPage(virtual_address="page2", content="Page 2"), 
             MemoryPage(virtual_address="page3", content="Page 3")]

    num_frames = 2  # Number of available memory frames

    fifo_page_faults = simulate_memory_management_fifo(pages, num_frames)
    print("FIFO Total Page Faults:", fifo_page_faults)

    lru_pae_faults = simulate_memory_management_lru(pages, num_frames)
    print("LRU Total Page Faults:", lru_pae_faults)

if __name__ == "__main__":
    main()
