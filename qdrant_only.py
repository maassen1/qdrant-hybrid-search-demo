from qdrant_client import models
from hybrid_searcher import HybridSearcher
import os


def main():

	hs = HybridSearcher(collection_name="startups", url=os.getenv("QDRANT_HOST"), api_key=os.getenv("QDRANT_API_KEY"))

	while True:

		user_input = ""
		try:
			user_input = str(input("What types of startups do you want to know about?: "))
			if user_input == "exit":
				break
		except:
			print("You did not enter a valid input, please try again.")

		query_filter = models.Filter(
	    	should=[
				models.FieldCondition(
					key="alt",
					match=models.MatchText(text=user_input)
					),
				models.FieldCondition(
					key="description",
					match=models.MatchText(text=user_input)
					),
				models.FieldCondition(
					key="city",
					match=models.MatchText(text=user_input)
					),

				]
		)
		cursor = hs.search(user_input, query_filter)

		print(f"Here's what I know about startups in the {user_input} space:")
		print("*" * 20)
		print("\n")
		for result in cursor:
			print(f"Name: {result['name']}")
			print(f"Description: {result['alt']}")
			print(f"Located in: {result['city']}")


if __name__ == "__main__":
	main()