class MemoryBlock:
    def __init__(self, size, allocated=False):
        self.size = size
        self.allocated = allocated

    def __repr__(self):
        return f"{'Allocated' if self.allocated else 'Free'} Block: {self.size} KB"


class BuddySystem:
    def __init__(self, total_memory):
        """Initialize the Buddy System with a total memory size."""
        self.total_memory = total_memory
        self.memory_blocks = [MemoryBlock(total_memory)]  # Start with a single block

    def allocate(self, request_size):
        """Allocate memory using the Buddy System."""
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

                # Mark the block as allocated                
                block.allocated = True  
                print(f"Allocated {request_size} KB.")
                return True

        print(f"Failed to allocate {request_size} KB. Not enough space.")
        return False

    def display_memory(self):
        """Display the current state of memory blocks."""
        print("Memory State:")
        for block in self.memory_blocks:
            status = "Allocated" if block.allocated else "Free"
            print(f" - 1 block of {block.size} KB ({status})")


if __name__ == "__main__":
    # Get total memory size from user
    total_memory_size = int(input("Enter the total memory size (in KB): "))
    buddy_system = BuddySystem(total_memory_size)

    # Display initial memory state
    print("Initial Memory State:")
    buddy_system.display_memory()

    # Allow the user to enter exactly three memory requests
    for i in range(3):
        request = input(f"Enter memory request size {i + 1} (in KB): ")
        try:
            request_size = int(request)
            buddy_system.allocate(request_size)
            buddy_system.display_memory()  # Display memory state after each allocation
        except ValueError:
            print("Please enter a valid integer.")

    # Final memory state
    print("\nFinal Memory State:")
    buddy_system.display_memory()
