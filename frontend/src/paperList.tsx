import { ExpandMore } from "@mui/icons-material";
import { Accordion, AccordionDetails, AccordionSummary, List, ListItemButton, Typography } from "@mui/material";

export type PaperInfo = {
  title: string;
  url: string;
};

export type PaperListProps = {
  papers: PaperInfo[];
  onClick: (url: string) => void;
};

export const PaperList = (props: PaperListProps) => {
  return (
    <Accordion>
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Typography>Paper List</Typography>
      </AccordionSummary>
      <AccordionDetails sx={{maxHeight: "300px", overflowY: "auto"}}>
        <List>
          {props.papers.map((paper, i) => (
            <ListItemButton
              key={i}
              onClick={() => props.onClick(paper.url)}
            >
              <Typography>{paper.title}</Typography>
            </ListItemButton>
          ))}
        </List>
      </AccordionDetails>
    </Accordion>
  )
};
