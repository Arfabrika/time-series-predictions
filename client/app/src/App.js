import React, {useState} from 'react';
import Button from '@mui/material/Button';
import FileUploader from './components/fileuploader';

function App() {
  // const [value, setValue] = useState("ABC")

  // function submit() {
  //   const url='https://jsonplaceholder.typicode.com/users';
  //   const user = {
  //     "name": "Ivan Ivanov",
  //     "username": "ivan2002",
  //     "email": "ivan2002@mail.com",
  //   };

  //   axios.post(url, user)
  //       .then(response => console.log(response.data))
  //       .catch(error => console.log(error));
  //   }

  return (
    <div className="App">
      <FileUploader></FileUploader>
      {/* <h1>AB</h1>
       <input type="file" id="selector" multiple></input>
       <Button variant="contained" onClick={submit}>Hello world</Button>
       <div>{value}</div> */}
    </div>
  );
}

export default App;
