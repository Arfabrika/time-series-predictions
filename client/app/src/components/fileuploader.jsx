import React, { useState } from 'react';
import axios from 'axios';

function FileUploader() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Выберите файл для загрузки');
      return;
    }

    try {
      setUploadStatus('Uploading...');

      const formData = new FormData(); // Создаем объект FormData для отправки данных

      formData.append('data', selectedFile); // Добавляем файл в FormData
      
      formData.append('needAvg', false);
      formData.append('learn_size', 0.7);
      formData.append('needAutoChoice', false);
      await console.log(formData);

      const response = await axios.post('http://localhost:8000/api/getInitData', formData,
    //   {
    //     "data": selectedFile,
    //     // "needAvg": true,
    //     // "learnSize": 0.7,
    //     // "data": [],
    //     // "algos": {
    //     //     "snaive": {
    //     //         "params": [1],
    //     //         "isPlot": true,
    //     //         "fullTrain": true
    //     //     },
    //     // }
    // }, 
    {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
      setUploadStatus('File uploaded successfully!');
      console.log('Server response:', response.data);
    } catch (error) {
      setUploadStatus('Failed to upload file');
      console.error('Upload failed:', error);
    }
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload</button>
      <p>{uploadStatus}</p>
    </div>
  );
}

export default FileUploader;