class MemoryBlock:
    def __init__(self, size, allocated=False, app_name=None):
        self.size = size
        self.allocated = allocated
        self.app_name = app_name  # Name of the application using the block

    def __repr__(self):
        status = f"Allocated to '{self.app_name}'" if self.allocated else "Free"
        return f"{status} Block: {self.size} KB"


class BuddySystem:
    def __init__(self, total_memory):
        """Initialize the Buddy System with a total memory size."""
        self.total_memory = total_memory
        self.memory_blocks = [MemoryBlock(total_memory)]  # Start with a single block

    def allocate(self, app_name, request_size):
        """Allocate memory using the Buddy System for a specific application."""
        # Find the smallest power of 2 that can satisfy the request
        size = 1
        while size < request_size:
            size *= 2

        # Find a suitable block
        for block in self.memory_blocks:
            if not block.allocated and block.size >= size:
                # Split the block if necessary
                while block.size > size:
                    buddy_size = block.size // 2
                    self.memory_blocks.append(MemoryBlock(buddy_size))  # Add new free block
                    block.size = buddy_size  # Reduce the size of the current block

                block.allocated = True  # Mark the block as allocated
                block.app_name = app_name
                print(f"Allocated {request_size} KB to '{app_name}'.")
                return True

        print(f"Failed to allocate {request_size} KB to '{app_name}'. Not enough space.")
        return False

    def display_memory(self):
        """Display the current state of memory blocks."""
        print("Current Memory State:")
        for block in self.memory_blocks:
            status = f"Allocated to '{block.app_name}'" if block.allocated else "Free"
            print(f" - 1 block of {block.size} KB ({status})")

    def release(self, app_name):
        """Release memory allocated to a specific application."""
        released = False
        for block in self.memory_blocks:
            if block.allocated and block.app_name == app_name:
                block.allocated = False
                block.app_name = None
                released = True
                print(f"Released memory from '{app_name}'.")
                break

        if not released:
            print(f"No memory found for application '{app_name}'.")
        else:
            # Attempt to merge adjacent free blocks
            self.merge_blocks()

    def merge_blocks(self):
        """Merge adjacent free blocks if they are buddies."""
        self.memory_blocks.sort(key=lambda b: b.size)  # Sort blocks by size
        i = 0
        while i < len(self.memory_blocks) - 1:
            current = self.memory_blocks[i]
            next_block = self.memory_blocks[i + 1]

            if not current.allocated and not next_block.allocated and current.size == next_block.size:
                # Merge the two blocks
                current.size *= 2
                self.memory_blocks.pop(i + 1)  # Remove the merged block
                print(f"Merged two {current.size // 2} KB blocks into one {current.size} KB block.")
            else:
                i += 1


if __name__ == "__main__":
    # Initialize the Buddy System with a total memory size (in KB)
    total_memory_size = int(input("Enter the total memory size for the server (in KB): "))
    buddy_system = BuddySystem(total_memory_size)

    # Display initial memory state
    print("\nInitial Memory State:")
    buddy_system.display_memory()

    while True:
        action = input("\nChoose an action - 'allocate', 'release', 'display', or 'exit': ").lower()
        if action == 'exit':
            break
        elif action == 'allocate':
            app_name = input("Enter application name: ")
            try:
                request_size = int(input(f"Enter memory request size for '{app_name}' (in KB): "))
                buddy_system.allocate(app_name, request_size)
            except ValueError:
                print("Please enter a valid integer for the memory size.")
        elif action == 'release':
            app_name = input("Enter application name to release memory: ")
            buddy_system.release(app_name)
        elif action == 'display':
            buddy_system.display_memory()
        else:
            print("Invalid action. Please try again.")

    # Final memory state
    print("\nFinal Memory State:")
    buddy_system.display_memory()
