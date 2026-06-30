import { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {

  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);

  async function askQuestion() {

    if (question.trim() === "") {
      return;
    }

    setLoading(true);

    try {

      const response = await axios.post(
        "http://127.0.0.1:5000/api/ask",
        {
          question: question,
        }
      );

      setAnswer(response.data.answer);
      setSources(response.data.sources);

    } catch (error) {

      console.log(error);

      setAnswer("Unable to connect to backend.");
      setSources([]);

    }

    setLoading(false);

  }

  return (

    <div className="container">

      <h1>📚 Local RAG Knowledge Assistant</h1>

      <textarea
        rows="6"
        placeholder="Ask a question..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
      />

      <button onClick={askQuestion}>
        Ask Question
      </button>

      {loading && <p>Loading...</p>}

      {answer && (
        <>
          <h2>Answer</h2>
          <p>{answer}</p>
        </>
      )}

      {sources.length > 0 && (

        <>

          <h2>Sources</h2>

          {sources.map((source, index) => (

            <div
              className="source-card"
              key={index}
            >

              <h3>{source.title}</h3>

              <p>{source.content}</p>

              <small>

                {source.metadata?.path}

              </small>

            </div>

          ))}

        </>

      )}

    </div>

  );

}

export default App;