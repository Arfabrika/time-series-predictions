import React, {useState} from 'react';
import Button from '@mui/material/Button';
import FileUploader from './components/fileuploader';
import SimpleOutput from './components/simpleoutput';
import AlgoMenu from './components/algomenu';
import AlgoParams from './components/algoparams';
import { algoNames } from './config';

function App() {
  const [postData, setPostData] = useState([]);

  const initialSelectedAlgorithms = algoNames.reduce((acc, algoName) => {
    acc[algoName] = false;
    return acc;
  }, {});

  const [selectedAlgorithms, setSelectedAlgorithms] = useState(initialSelectedAlgorithms);


  const handleDataFetched = (data) => {
    setPostData(data);
  };

  return (
    <div className="App">
      <AlgoMenu selectedAlgorithms={selectedAlgorithms} setSelectedAlgorithms={setSelectedAlgorithms}></AlgoMenu>
      <AlgoParams parameters={['qwe', 'wer']}></AlgoParams>
      <FileUploader onDataFetched={handleDataFetched}></FileUploader>
      <SimpleOutput data={postData}></SimpleOutput>
    </div>
  );
}

export default App;
