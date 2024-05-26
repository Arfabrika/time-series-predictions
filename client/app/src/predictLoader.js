
import axios from "axios";

export class PredictLoader {
  static async getData(selectedFile, needAvg = false, learn_size = 0.7, needAutoChoice = false, algos = {}) {
      const formData = new FormData();

      formData.append('data', selectedFile);      
      formData.append('needAvg', needAvg);
      formData.append('learn_size', learn_size);
      formData.append('needAutoChoice', needAutoChoice);
      formData.append('algos_str', 
      JSON.stringify({
        "snaive": {
          "params": [1],
          "isPlot": true,
          "fullTrain": true
          },
        "AR": {
          "params": [7],
          "isPlot": true,
          "fullTrain": true
          }
      }));

    const response = await axios.post('http://localhost:8000/api/predict', formData,
    {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      });
    return response;
  }
}