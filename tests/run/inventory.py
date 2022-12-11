from pyconfman.models.inventory import Group, Host

host1 = Host(
    name="host1.example.com",
)

host2 = Host(name="host2.example.com")

group1 = Group("group1", {host1, host2})

group2 = Group("group2", {group1, host1})


host3 = Host("Test")
