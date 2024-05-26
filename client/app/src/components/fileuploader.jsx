import React, { useState } from 'react';
import { PredictLoader } from '../predictLoader';
import { Button } from '@mui/material';
import { styled } from '@mui/material/styles';

const VisuallyHiddenInput = styled('input')({
  clip: 'rect(0 0 0 0)',
  clipPath: 'inset(50%)',
  height: 1,
  overflow: 'hidden',
  position: 'absolute',
  bottom: 0,
  left: 0,
  whiteSpace: 'nowrap',
  width: 1,
});


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
      setUploadStatus('Производятся вычисления...');
      const response = await PredictLoader.getData(selectedFile)
      await onDataFetched(response.data)
      setUploadStatus('Вычисления завершены');
    } catch (error) {
      setUploadStatus('Ошибка при вычислениях');
      console.error('Upload failed:', error);
    }
  };

  return (
    <div style={{alignItems: "center", justifyContent: "center"}}>
      <p>Загрузите файл с временным рядом</p>
      <Button
        component="label"
        role={undefined}
        variant="contained"
        tabIndex={-1}
        onChange={handleFileChange}
      >
        Загрузить файл
        <VisuallyHiddenInput type="file" />
      </Button>
      <br/>
      <br/>
      <Button 
      onClick={handleUpload}
      variant="contained"
      >Начать прогнозирование</Button>
      <p>{uploadStatus}</p>
    </div>
  );
}

export default FileUploader;