from time import strftime, sleep, time
import os
import flet
from flet import *
from flet.auth.providers import GoogleOAuthProvider
import requests

PAGE_TITLE = "Rental Resource Management System"

provider = GoogleOAuthProvider(
    client_id="510860766543-qq5c159h5u7j5dcuebi248sl5dvim66c.apps.googleusercontent.com",
    client_secret="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",
    redirect_url="http://localhost:8550/api/oauth/redirect",
)


def get_data():
    response = requests.get("http://127.0.0.1:8000/get_data")
    return response.json().get("data")


data = get_data()


def main(page: Page):
    login_page = LoginPage(page)
    page.on_login = login_page.on_login
    page.on_logout = login_page.on_logout
    email = login_page.email
    name = login_page.uname
    page.add()
    data = fetch_data()

    page.padding = 50
    t = Tabs(
        selected_index=0,
        animation_duration=0,
        tabs=[
            Tab(
                text="Items",
                icon=icons.LIST,
                content=data,
            ),
            Tab(
                text="My Listed Items",
                icon=icons.LIBRARY_ADD,
            ),
            Tab(
                text="Rented Items",
                icon=icons.CAR_RENTAL_ROUNDED,
                content=Container(
                    content=Text("Coming Soon"), alignment=alignment.center
                ),
            ),
        ],
        expand=1,
    )
    t.visible = False  # Hide the tabs initially
    page.tabs = t
    page.add(t)

    wait_count = 30
    while email == "->" or name == "->":
        sleep(1)
        email = login_page.email
        name = login_page.uname

        wait_count -= 1
        if wait_count == 0:
            login_page.login_button_click(None)

    print(email, name)
    t.tabs[1].content = my_RRMSAPP(page, email, name, t)
    page.update()

    while True:
        sleep(5)
        print("refreshing")
        t.tabs[0].content = fetch_data()
        page.update()


def fetch_data(forme: bool = False, email: str = None):
    data = get_data()
    column = [
        DataColumn(Text("User Name")),
        DataColumn(Text("Product Name")),
        DataColumn(Text("Price")),
        DataColumn(Text("Phone No")),
        DataColumn(Text("Email")),
        DataColumn(Text("Availability")),
        DataColumn(Text("Time Added")),
    ]
    row = []

    if forme:
        dataaa = [i for i in data if i["email"] == str(email)]
        for i in dataaa:
            row.append(
                DataRow(
                    [
                        DataCell(Text(i["username"])),
                        DataCell(Text(i["product_name"])),
                        DataCell(Text(i["price"])),
                        DataCell(Text(i["phone"])),
                        DataCell(Text(i["email"])),
                        DataCell(
                            Text("Available" if i["availability"] else "Not Available")
                        ),
                        DataCell(Text(i["time_added"])),
                    ]
                )
            )
    else:
        print("---", data)
        for i in data:
            row.append(
                DataRow(
                    [
                        DataCell(Text(i["username"])),
                        DataCell(Text(i["product_name"])),
                        DataCell(Text(i["price"])),
                        DataCell(Text(i["phone"])),
                        DataCell(Text(i["email"])),
                        DataCell(
                            Text("Available" if i["availability"] else "Not Available")
                        ),
                        DataCell(Text(i["time_added"])),
                    ],
                )
            )

    return DataTable(columns=column, rows=row)


class my_RRMSAPP(UserControl):
    def __init__(self, page: Page, email, name, t):
        super().__init__()
        self.page = page
        self.email = email
        self.name = name
        self.t = t

    def build(self):
        self.ItemName = TextField(hint_text="Item Name", expand=True)
        self.ItemPrice = TextField(hint_text="Item Price", expand=True)
        self.PhoneNo = TextField(hint_text="Phone No", expand=True)

        self.tasks = Column()
        self.data = fetch_data(True, self.email)
        return [
            Column(
                controls=[
                    Row(
                        controls=[
                            self.ItemName,
                            self.ItemPrice,
                            self.PhoneNo,
                            FloatingActionButton(
                                icon=icons.ADD, on_click=self.add_clicked
                            ),
                        ],
                    ),
                    Column(
                        spacing=25,
                        controls=[
                            self.tasks,
                            self.data,
                        ],
                    ),
                ],
            )
        ]

    def update(self, e):
        self.data = fetch_data(True, self.email)
        self.page.update()

    def add_clicked(self, e):
        print("clicked")

        task = {
            "username": self.name,
            "product_name": self.ItemName.value,
            "price": self.ItemPrice.value,
            "email": self.email,
            "availability": True,
            "phone": self.PhoneNo.value,
            "time_added": time(),
        }
        res = requests.post(
            f"http://127.0.0.1:8000/insert_data?username={task['username']}&product_name={task['product_name']}&price={task['price']}&email={task['email']}&availability={task['availability']}&phone={task['phone']}"
        )
        self.t.tabs[1].content = my_RRMSAPP(self.page, self.email, self.name, self.t)

    def task_delete(self, task):
        self.tasks.controls.remove(task)
        self.update()


class LoginEvent:
    def __init__(self, error):
        self.error = error


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.PAGE_TITLE = "RRMS"
        self.uname = "->"
        self.email = "->"
        # Add a variable to track login status
        self.logged_in = False
        self.login_button = ElevatedButton(
            "Login with Google",
            on_click=self.login_button_click,
            bgcolor="green",
            color="white",
        )
        self.logout_button = ElevatedButton(
            "Logout",
            on_click=self.logout_button_click,
            bgcolor="blue",
            color="white",
        )
        self.logout_button.visible = False
        self.page.title = PAGE_TITLE
        self.page.dark_theme = theme.Theme(
            color_scheme_seed=colors.INDIGO, use_material3=True
        )
        self.page.padding = 50
        self.page.appbar = AppBar(
            leading=Icon(icons.HOME),
            leading_width=40,
            title=Text(self.PAGE_TITLE),
            center_title=False,
            actions=[self.logout_button],
        )
        page.add(
            Column(
                [
                    Row(
                        [
                            Container(
                                content=Column(
                                    [
                                        self.login_button,
                                    ]
                                )
                            )
                        ],
                        alignment="center",
                    )
                ],
                alignment="center",
            )
        )
        self.page.update()

    def login_button_click(self, e):
        self.page.login(provider)

    def on_login(self, e: LoginEvent):
        self.logged_in = True  # Update the login status
        self.login_button.visible = False
        self.uname = str(self.page.auth.user["name"])
        self.email = str(self.page.auth.user["email"])
        self.logout_button.visible = True
        self.page.tabs.visible = True  # Show the tabs on successful login
        self.page.update()

    def logout_button_click(self, e: LoginEvent):
        self.page.logout()

    def on_logout(self, e):
        self.uname = "->"
        self.email = "->"
        self.logged_in = False  # Update the login status
        self.login_button.visible = True
        self.logout_button.visible = False
        self.page.tabs.visible = False  # Hide the tabs on logout
        self.page.update()


flet.app(target=main, port=8550, view=flet.WEB_BROWSER)
