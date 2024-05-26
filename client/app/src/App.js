import React, {useState} from 'react';
import FileUploader from './components/fileuploader';
import SimpleOutput from './components/simpleoutput';
import AlgoMenu from './components/algomenu';
import AlgoParams from './components/algoparams';
import { algoNames, algoParamsList } from './config';
import './style/App.css'
import InputParamField from './components/inputparamfiled';
import { Checkbox, Container, FormControlLabel } from '@mui/material';
import AlgoOut from './components/algoout';

function App() {
  const [postData, setPostData] = useState([]);

  const initialSelectedAlgorithms = algoNames.reduce((acc, algoName) => {
    acc[algoName] = false;
    return acc;
  }, {});

  const [selectedAlgorithms, setSelectedAlgorithms] = useState(initialSelectedAlgorithms);
  const [selectedMenuItemIndex, setSelectedMenuItemIndex] = useState(-1);
  const [paramsValues, setParamsValues] = useState(Array(algoParamsList.length).fill({}));
  const [learnSize, setLearnSize] = useState(0);

  // Функция обратного вызова для изменения значения параметра
  const handleParamChange = (parameterName, value) => {
    setParamsValues(prevStates => {
      const newStates = [...prevStates];
      newStates[selectedMenuItemIndex] = {
        ...newStates[selectedMenuItemIndex],
        [parameterName]: value,
      };
      return newStates;
    });
  };


  const handleDataFetched = (data) => {
    setPostData(data);
  };

  const handleMenuItemSelect = (index) => {
    setSelectedMenuItemIndex(index);
  };

  const handleLearnSize = (value) => {
    setLearnSize(value);
  };

  return (
    <Container className="App">
      <h2>Прогнозирование временных рядов</h2>
      <div className="algo_module">
        <AlgoMenu 
        selectedAlgorithms={selectedAlgorithms} 
        setSelectedAlgorithms={setSelectedAlgorithms}
        onMenuItemSelect={handleMenuItemSelect}
        ></AlgoMenu>
        <AlgoParams
        key={selectedMenuItemIndex} 
        parameters={algoParamsList[selectedMenuItemIndex]}
        onChangeParam={handleParamChange}
        values={paramsValues[selectedMenuItemIndex]}/>
      </div>
      <br/>
      <br/>
      <InputParamField
        name='learn_size'
        onChange={handleLearnSize}
      />
      <FormControlLabel control={<Checkbox />} label="Расчет среднего прогнозов" />
      <FormControlLabel control={<Checkbox />} label="Нужен автоматический выбор алгоритма" />
      {console.log("start---\n")}
      {Object.keys(paramsValues).forEach(key => {
          console.log(key);
          Object.keys(paramsValues[key]).forEach(key2 => {
            console.log(key2 + ": " + paramsValues[key][key2]);
          })
        })}
        {console.log("stop---\n")}
        
      <FileUploader onDataFetched={handleDataFetched}/>
      <br/>
      <br/>
      {
        Object.hasOwn(postData, "isStat") ?
        <div>
          <h2>Результаты прогнозирования</h2>
          <br/>
          <AlgoOut data={postData}/>
        </div>
        : ""
      }
    </Container>
  );
}

export default App;
