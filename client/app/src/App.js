import React, {useState} from 'react';
import FileUploader from './components/fileuploader';
import SimpleOutput from './components/simpleoutput';
import AlgoMenu from './components/algomenu';
import AlgoParams from './components/algoparams';
import { algoNames, algoParamsList } from './config';
import './style/App.css'

function App() {
  const [postData, setPostData] = useState([]);

  const initialSelectedAlgorithms = algoNames.reduce((acc, algoName) => {
    acc[algoName] = false;
    return acc;
  }, {});

  const [selectedAlgorithms, setSelectedAlgorithms] = useState(initialSelectedAlgorithms);
  const [selectedMenuItemIndex, setSelectedMenuItemIndex] = useState(-1);
  const [paramsValues, setParamsValues] = useState(Array(algoParamsList.length).fill({}));

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

  return (
    <div className="App">
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
      {console.log("start---\n")}
      {Object.keys(paramsValues).forEach(key => {
          console.log(key);
          Object.keys(paramsValues[key]).forEach(key2 => {
            console.log(key2 + ": " + paramsValues[key][key2]);
          })
        })}
        {console.log("stop---\n")}
        
      <FileUploader onDataFetched={handleDataFetched}/>
      <SimpleOutput data={postData}/>
    </div>
  );
}

export default App;
