import { Button, TextField } from '@mui/material';
import rehypeKatex from 'rehype-katex';
import remarkMath from "remark-math";
import "katex/dist/katex.min.css";
import ReactMarkdown from 'react-markdown';

function App() {
  return (
    <div style={{width: "100%", maxWidth: "800px"}}>
      <div style={{display: "flex"}}>
        <TextField label={"URL"} sx={{flexGrow: 1}} />
        <Button variant="outlined">Translate</Button>
      </div>

      <ReactMarkdown remarkPlugins={[remarkMath]} rehypePlugins={[rehypeKatex]}>
        $x + y$
      </ReactMarkdown>
    </div>
  );
}

export default App;
