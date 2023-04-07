import csv
import sys


class Item:
    def __init__(self, item: dict):
        self.item = item["Item"]
        self.stock = int(item["Current Stock"])
        self.price = float(item["Price per Item"])
        self.previous_sales = int(item["Previous Sales"])
        self.today_sales = 0
        self.lost_sales = 0

    def updated_dict(self):
        return {
            "Item": self.item,
            "Current Stock": self.stock,
            "Price per Item": self.price,
            "Previous Sales": self.previous_sales,
        }


class Stock:
    def __init__(self, file_name, output_file):
        """
            Initialize the Stock class.
            :param file_name: name of the input file.
            :param output_file: name of the output file.
        """
        self.file_name = file_name
        self.output_file = output_file
        self.items: list[Item] = []
        self.sold_items = set()

    def user_prompt(self):
        """
            Prompt the user to input item.
            :return: user input
        """
        return input(f'Select a number (1-{len(self.items)}) to indicate a sale, or e to indicate end of day:')

    @staticmethod
    def count_trend(previous_sales: int, current_sales: int) -> float:
        """
            Count the trend of the current day's sales.
            :param previous_sales: item of the previous day's sales
            :param current_sales: item of the current day's sales
            :return: total trend.
        """
        total_trend = ((current_sales - previous_sales) / previous_sales) * 100
        return total_trend

    @staticmethod
    def avg_demand(previous_sales: int, current_sales: int) -> int:
        """
            Calculate the average demand.
            :param previous_sales: item of the previous day's sales.
            :param current_sales: item of the current day's sales.
            :return: average demand.
        """
        average = (previous_sales + current_sales) / 2
        if average.is_integer():
            return int(average)
        else:
            return int(average) + 1

    @staticmethod
    def twenty_percent(demand: int):
        total = demand * 0.2
        total_decimal = total - int(total)
        if total_decimal > 0.5:
            return int(total) + 1
        else:
            return int(total)

    @staticmethod
    def get_warehouse(current_stock: int, avg_demand: int) -> int:
        """
                Calculate the warehouse inventory.
                :param current_stock: item of the current stock.
                :param avg_demand: item of the average demand.
                :return: warehouse inventory.
        """
        return 0 if current_stock > avg_demand else avg_demand - current_stock

    def read_file(self) -> list:
        """
            Read the CSV file.
            list_data.
            :return: list of csv item.
        """
        with open(self.file_name, "r") as f:
            reader = csv.DictReader(f)
            item = list(reader)
            for d in item:
                item = Item(item=d)
                self.items.append(item)
        return self.items

    def modify_to_write(self):
        """
                Modify the item to be written to the output CSV file.
        """
        for item in self.items:
            demand = item.today_sales + item.lost_sales
            demand_percent = self.twenty_percent(demand)
            total_demand = demand + demand_percent
            wh_stock = self.get_warehouse(current_stock=item.stock, avg_demand=total_demand)
            item.stock += wh_stock
            item.previous_sales = item.today_sales

    def write_csv(self):
        """
               Write the item to the output CSV file.
       """
        s.modify_to_write()  # modify list_data before write.
        fieldnames = self.items[0].updated_dict().keys() if self.items else []
        with open(self.output_file, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for item in self.items:
                writer.writerow(item.updated_dict())

    def sell_item(self, item_number: int) -> bool:
        """
            Function to validate sales and modify item stock after sale.
            :param item_number:
            :return:
        """
        self.sold_items.add(item_number)  # store item in today sold item set.
        item = self.items[item_number - 1]
        if item.stock <= 0:
            print(f"We're out of {item.item}!")
            item.lost_sales += 1
            return False
        item.stock -= 1  # modify the stock.
        item.today_sales += 1
        return True

    def initiate_table(self):
        """
            Print initial item after reading the CSV file.
        """
        print(f"{'#': ^3} {'Item':<15} {'Current Stock':^15} {'Price per Item':>15}")
        print('-' * 51)
        for (sr_no, item) in enumerate(self.items, 1):
            print(f"{sr_no:<3} {item.item:<15} {item.stock:^15} {item.price:>15}")

    def print_today_sales(self):
        """
            Print item of sold items for the day.
        """
        print(f"{'Total Sales':<47}")
        print(f"{'#':<3} {'Item':<15} {'Sales':^5} {'$ / Item':^10} {'Total':>10}")
        print("=" * 47)
        sum_price = 0
        for (sr_no, item) in enumerate(self.items, 1):
            if sr_no in self.sold_items:
                total_price = float(item.today_sales) * item.price
                sum_price += total_price
                print(
                    f"{sr_no:<3} {item.item:<15} {item.today_sales:^5} {item.price:^10} {total_price:>10.2f}")
        print(f"{'TOTAL':<10}{sum_price:>37.2f}")

    def print_lost_sales(self):
        """
            Print trends for the sold items for the day.
        """
        total = 0
        print(f"{'Lost Sales':<60}")
        print(f"{'#':<3} {'Item':<15} {'Sales':^8} {'Price Per Item':^20} {'Trend':>10}")
        print('-' * 60)
        for (sr_no, item) in enumerate(self.items, 1):
            if sr_no in self.sold_items:
                item_total = item.price * item.lost_sales
                total += item_total
                print(
                    f"{sr_no:<3} {item.item:<15} {item.lost_sales:^8} {item.price:^15} {item_total:>10.2f}")
        print(f"{'TOTAL':<26}{total:>29.2f}")

    def print_restock(self):
        """
            print item of the sold items that needs to be re-stock from the warehouse.
        """

        """
        Restock
        # Item Demand 20% Total Demand Current Stock From Warehouse
        """
        print(f"{'Restock':<100}")
        print(
            f"{'#':<4} {'Item':<15} {'Demand':^15} {'20%':^15} {'Total Demand':>15} {'Current Stock':>15} {'From Warehouse':>15}")
        print('-' * 100)
        for (sr_no, item) in enumerate(self.items, 1):
            if sr_no in self.sold_items:
                demand = item.today_sales + item.lost_sales
                demand_percent = self.twenty_percent(demand)
                total_demand = demand + demand_percent
                item_warehouse = self.get_warehouse(current_stock=item.stock, avg_demand=total_demand)
                print(
                    f"{sr_no:<4} {item.item:<15} {demand:^15} {demand_percent:^15} {total_demand:>15} {item.stock:>15} {item_warehouse :>15}")


if __name__ == "__main__":
    arguments = sys.argv[1::]
    if len(arguments) != 2:  # check if both files are provided in args
        print("Usage: python main.py <input_file> <output_file>")
    else:
        input_filename = arguments[0]  # get input file name
        output_filename = arguments[1]  # get output file name

        s = Stock(file_name=input_filename, output_file=output_filename)  # initiate class with the given files.
        s.read_file()  # read file item.
        s.initiate_table()  # print initial item after reading file.
        while True:
            user_input = s.user_prompt()
            if user_input.lower() == 'e':  # if `e` print all three tables and store item.
                s.print_today_sales()
                s.print_lost_sales()
                s.print_restock()
                s.write_csv()
                break
            else:
                if user_input.isdigit():
                    user_input = int(user_input)
                    valid_range = len(s.items)
                    if 1 <= user_input <= valid_range:
                        s.sell_item(user_input)
                    else:
                        print(f"Error: Enter a valid number between 1 and {valid_range}.")
                else:
                    print("Error: Enter a valid number.")
