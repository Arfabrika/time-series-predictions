import React, { useState } from 'react';
import axios from 'axios';
import { PredictLoader } from '../predictLoader';

function FileUploader({ onDataFetched }) {
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
      const response = await PredictLoader.getData(selectedFile)
      await onDataFetched(response.data)
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