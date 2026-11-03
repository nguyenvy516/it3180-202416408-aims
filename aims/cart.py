MAX_NUMBERS_ORDERED = 20


class Cart:
    '''Giỏ hàng chứa tối đa MAX_NUMBERS_ORDERED đĩa DVD.'''

    def __init__(self):
        self.items = []

    def add_dvd(self, dvd):
        if len(self.items) >= MAX_NUMBERS_ORDERED:
            print("The cart is almost full")
            return False
        self.items.append(dvd)
        print(f"Đã thêm đĩa '{dvd.title}' vào giỏ hàng")
        return True

    def remove_dvd(self, dvd):
        if dvd in self.items:
            self.items.remove(dvd)
            print("The disc has been removed")
            return True
        print("The disc is not in the cart")
        return False

    def total_cost(self):
        return sum(item.cost for item in self.items)

    def total_cost_with_discount(self, percent=0):
        if percent < 0 or percent > 100:
            raise ValueError("Discount percentage must be between 0 and 100")
        total = self.total_cost()
        return total * (100 - percent) / 100

    def print_cart(self):
        if not self.items:
            print("The cart is empty")
            return
        print("***********************CART***********************")
        print("Ordered Items:")
        for i, item in enumerate(self.items, 1):
            print(f"{i}. {item}")
        print(f"Total cost: {self.total_cost():.2f} $")
        print("***************************************************")

    def sort_by_title(self):
        '''Sắp xếp các đĩa trong giỏ hàng theo tiêu đề (alphabet), nếu trùng theo giá giảm dần.'''
        self.items.sort(key=lambda item: (item.title.lower(), -item.cost))

    def sort_by_cost(self):
        '''Sắp xếp các đĩa trong giỏ hàng theo giá giảm dần, nếu trùng theo tiêu đề.'''
        self.items.sort(key=lambda item: (-item.cost, item.title.lower()))
