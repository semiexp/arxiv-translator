import axios from "axios";
import { Button, CircularProgress, TextField } from '@mui/material';
import { useEffect, useState } from 'react';
import rehypeKatex from 'rehype-katex';
import remarkMath from "remark-math";
import "katex/dist/katex.min.css";
import ReactMarkdown from 'react-markdown';

import { PaperList } from "./paperList";

function App() {
  const [url, setUrl] = useState("");
  const [text, setText] = useState("");
  const [error, setError] = useState("");
  const [isRunning, setIsRunning] = useState(false);

  const [paperList, setPaperList] = useState<{title: string, url: string}[]>([]);

  const updatePaperList = async () => {
    const response = await axios.get("http://localhost:8090/list");

    setPaperList(response.data["response"]);
  };

  const runTranslate = async () => {
    if (isRunning) {
      return;
    }

    setIsRunning(true);
    setError("");
    setText("");

    const response = await axios.post("http://localhost:8090/markdown", {arxiv_url: url}, {headers: {"Content-Type": "application/json"}});

    setIsRunning(false);

    if (response.data["error"]) {
      setText("");
      setError(response.data["error"]);
    } else {
      setText(response.data["response"]);
      setError("");
    }

    updatePaperList();
  };

  useEffect(() => {
    updatePaperList();
  }, []);

  const selectPaperFromList = async (url: string) => {
    setUrl(url);
    runTranslate();
  };

  return (
    <div style={{width: "100%", maxWidth: "800px"}}>
      <div style={{display: "flex"}}>
        <TextField label={"URL"} value={url} sx={{flexGrow: 1}} onChange={(e) => setUrl(e.target.value)} />
        <Button variant="outlined" onClick={runTranslate} disabled={isRunning}>Translate</Button>
      </div>

      <PaperList papers={paperList} onClick={(url) => selectPaperFromList(url)} />

      {
        isRunning && <CircularProgress />
      }
      {
        error && <div>{error}</div>
      }
      {
        (!isRunning && error === "") && (
          <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
            {text}
          </ReactMarkdown>
        )
      }
    </div>
  );
}

export default App;
