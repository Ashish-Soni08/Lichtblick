# Lichtblick Multi-Agent System

This directory contains a multi-agent system implementation for the Lichtblick German learning assistant using the OpenAI Agents SDK. The system uses three specialized agents working together to provide comprehensive German language learning assistance.

## Architecture

The multi-agent system consists of three agents:

1. **Orchestration Agent (Lichtblick)**: The main agent that interacts with users, coordinates the specialized agents, and combines their outputs into a comprehensive response.

2. **Vocabulary Extraction Agent**: Specializes in extracting German vocabulary from text and providing English translations in a format suitable for flashcard applications.

3. **Sentence Analysis Agent**: Specializes in translating and analyzing German sentences, providing grammatical breakdowns and explanations.

## Files

- `lichtblick.py`: Contains the implementation of the three agents and their coordination logic, along with a simple example usage.
- `vibe_coding_context/`: Directory containing reference materials for the implementation.

## Usage

### Prerequisites

1. Install the required dependencies:
   ```
   pip install openai-agents python-dotenv
   ```

2. Create a `.env` file in the project root with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Running the System

The current implementation provides a basic function to interact with the Lichtblick agent:

```python
# Import the function from lichtblick.py
from lichtblick import submit_user_msg
import asyncio

# Example usage
async def main():
    text = "Die Katze liegt gemütlich auf dem Sofa."
    result = await submit_user_msg(text)
    print(result)

asyncio.run(main())
```

## Example Output

```
🤖 Vocabulary Extraction:
die (->) the
Katze (->) cat
liegt (->) lies/is lying
gemütlich (->) comfortably
auf (->) on
dem (->) the
Sofa (->) sofa

🤖 Sentence Analysis:
The cat is lying comfortably on the sofa.

Die (->) the (feminine nominative singular definite article)
Katze (->) cat (feminine noun, nominative case)
liegt (->) is lying (third-person singular present tense of "liegen")
gemütlich (->) comfortably (adjective/adverb)
auf (->) on (preposition taking the dative case here)
dem (->) the (masculine/neuter dative singular definite article)
Sofa (->) sofa (neuter noun, dative case)

🤖 What else would you like to learn about German?
```

## Extending the System

To extend the system with additional capabilities:

1. Define new specialized agents with specific instructions in `lichtblick.py`.
2. Add the new agents to the tools list of the orchestration agent.
3. Update the `submit_user_msg` function if needed to handle new types of interactions.

## Notes

- The system uses the OpenAI Agents SDK for structured agent interactions.
- The orchestration agent maintains a friendly, supportive tone specified in its instructions.
- All agents follow specific rules, such as starting responses with 🤖 and maintaining an encouraging tone.
- The implementation uses environment variables for API key management through python-dotenv.