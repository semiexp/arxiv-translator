import axios from "axios";
import { Button, TextField } from '@mui/material';
import { useState } from 'react';
import rehypeKatex from 'rehype-katex';
import remarkMath from "remark-math";
import "katex/dist/katex.min.css";
import ReactMarkdown from 'react-markdown';

function App() {
  const [url, setUrl] = useState("");
  const [text, setText] = useState("");

  const runTranslate = async () => {
    const response = await axios.post("http://localhost:8090/markdown", {arxiv_url: url}, {headers: {"Content-Type": "application/json"}});
    setText(response.data["response"]);
  };

  return (
    <div style={{width: "100%", maxWidth: "800px"}}>
      <div style={{display: "flex"}}>
        <TextField label={"URL"} value={url} sx={{flexGrow: 1}} onChange={(e) => setUrl(e.target.value)} />
        <Button variant="outlined" onClick={runTranslate}>Translate</Button>
      </div>

      <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
        {text}
      </ReactMarkdown>
    </div>
  );
}

export default App;
