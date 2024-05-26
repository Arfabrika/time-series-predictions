import React, {useState} from 'react';
import { Button } from '@mui/material';

function AlgoOutItem({ data, isBest }) {

  const [fullImg, setFullImg] = useState(false);

  const handleClick = () => {
    setFullImg(!fullImg);
  };

  return (
    <div style={{border: "1px solid", marginTop: "5px", paddingLeft:"20px"}}>
      {data ?
        <div>
        {
          isBest ?
          <div style={{textAlign: "center"}}>
            <h3 style={{textAlign: "center", font: "red"}}>Лучший алгоритм</h3>
            <h4 style={{textAlign: "center"}}>{data.name}</h4>
          </div>
          : <h4 style={{textAlign: "center"}}>{data.name}</h4>
        }
        <p>Параметры: ({data.params})</p>
        <p>Метрики:</p>
          <ul>
            {Object.entries(data.metrics).map(([key, value]) => (
              <li key={key}>{key}: {value}</li>
            ))}
          </ul>
          {data.plot ?
            <div>
                <p>График:</p>
                <img 
                src={fullImg ? `data:image/png;base64,${data.fullPlot}`: `data:image/png;base64,${data.plot}`} 
                alt={`Ошибка с графиком`}
                onClick={handleClick} />
            </div>
            : ""
          }
          <br/>
          {/* <div style={{display: "flex"}}>
             <Button 
          variant="contained"
          sx={{ justifyContent: "center"}}
          >Скачать результаты прогнозирования</Button>
          </div>
          <br/> */}
        </div>
        : "Ошибка при передаче данных"}
    </div>
  );
}

export default AlgoOutItem;