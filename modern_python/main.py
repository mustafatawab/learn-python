# from dotenv import load_dotenv
# load_dotenv()
# import os

# api_key = os.getenv('GEMINI_API_KEY')
# print(api_key)


def row(row : list[str]) -> None:
    print(" and ".join(row))




def main() -> None:

    x = ['a' , 'b' , 'c']
    y = ("t1 " , "t2")
    row(x)
    row(y)


main()