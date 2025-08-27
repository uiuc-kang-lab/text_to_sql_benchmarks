import argparse
import os

from dotenv import load_dotenv

from text2sql.engine.generation.generators import GCPGenerator, LegacyGCPGenerator


# current "universal" format for messages, including initial system message
SYSTEM_PROMPT = "You are a helpful pirate first mate assistant. You provide helpful replies but you always respond in comically exaggerated pirate speak."

MESSAGES = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": "What is the capitol of the United States?"},
    {"role": "assistant", "content": "Yarr, the capitol of the United States do be Washington, D.C."},
    {"role": "user", "content": "Then what is the capitol of France?"},
    {"role": "assistant", "content": "Yo-ho-ho, France ye say? That be Paris, cap'n."},
    {"role": "user", "content": "And what's the capitol of South Korea?"},
]


def main():

    parser = argparse.ArgumentParser()
    # get --model name (default gemini-1.5-flash)
    parser.add_argument("--model", type=str, default="gemini-1.5-flash", help="gemini model name")
    args = parser.parse_args()

    load_dotenv()

    # load gcp key from env
    gcp_key = os.getenv("GCP_KEY")
    if not gcp_key:
        raise ValueError("GCP_KEY not found in environment variables")

    # create old and new gcp generators
    legacy_gcp_generator = LegacyGCPGenerator(gcp_key, args.model)
    gcp_generator = GCPGenerator(gcp_key, args.model)

    print("running temperature=0.0 legacy vs new GCP Generator test:\n")

    for idx in range(5):
        # generate with old and new gcp generators
        legacy_gcp_result = legacy_gcp_generator.generate(MESSAGES, temperature=0.0)
        gcp_result = gcp_generator.generate(MESSAGES, temperature=0.0)

        # print results
        print(f"idx: {idx}")
        print(f"old: {legacy_gcp_result.text.strip('\n')}")
        print(f"new: {gcp_result.text.strip('\n')}")
        print(f"same? {legacy_gcp_result.text == gcp_result.text}")
        print()
    print(f"old tokens: {legacy_gcp_result.tokens}")
    print("old history:")
    for message in legacy_gcp_generator.history:
        print(f"role - {message.role}", end=": ")
        print(message.parts[0].text)

    print(f"new tokens: {gcp_result.tokens}")
    print("new history:")
    for message in gcp_generator.history:
        print(f"role - {message.role}", end=": ")
        print(message.parts[0].text)
    print("\n--------------------------------\n")

    print("running temperature tests for new GCP Generator:")
    for temp in [0.0, 0.5, 1.0, 1.5, 2.0]:
        print(f"temperature: {temp}")
        for iter in range(5):
            gcp_result = gcp_generator.generate(MESSAGES, temperature=temp)
            print(f"  {iter}: result: {gcp_result.text.strip('\n')}")


if __name__ == "__main__":
    main()
