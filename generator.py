import random
import csv

# def load_tags(filename):
#     with open(filename, "r") as csvfile:
#         reader = csv.reader(csvfile)
#         rows = list(reader)[1:]
#         for row in rows:
#             t = Tag.objects.create(
#                 title=row[0],
#             )
#             print(t)


# load_tags("tags.csv")


# n_users = 5
# users = []
# for _ in range(n_users):
#     user = User.objects.create(
#         email="abc{}@abc.com".format(_),
#         first_name="Example {}".format(_),
#         last_name="User {}".format(_),
#         password="llave5012",
#     )
#     Profile.objects.create(user=user)
#     users.append(user)
#     print("New user create", user.email)


def load_post(filename):

    with open(filename, "r") as csvfile:
        reader = csv.reader(csvfile)
        rows = list(reader)[1:]
        tags = Tag.objects.all()
        tags = random.choices(tags, k=random.randint(1, 20))

        for author in random.choices(users, k=random.randint(1, 10)):
            author = author

            for row in rows:
        
                t = Post.objects.create(
                    title=row[0], author=author, content=row[2], status=1
                )
                t.tags.set(tags)

                print(t.author)

load_post("post.csv")
