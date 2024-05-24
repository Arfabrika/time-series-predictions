import React, { useState } from 'react';
import { TextField, Button, Grid, Container } from '@mui/material';

const AlgoParams = ({ parameters }) => {
  // Состояние для хранения значений параметров
  const [values, setValues] = useState({});

  // Обработчик изменений значения параметра
  const handleChange = (parameterName, value) => {
    setValues(prevValues => ({
      ...prevValues,
      [parameterName]: value,
    }));
  };

  // Обработчик отправки формы
  const handleSubmit = (event) => {
    event.preventDefault();
    // Здесь вы можете выполнить действия с отправленными данными, например, отправить их на сервер
    console.log('Submitted values:', values);
  };

  return (
    <Container>
      <form onSubmit={handleSubmit}>
        <Grid container spacing={2}>
          {parameters.map((parameter, index) => (
            <Grid item xs={12} key={index}>
              <TextField
                label={parameter}
                variant="outlined"
                fullWidth
                margin="normal"
                value={values[parameter] || ''}
                onChange={(e) => handleChange(parameter, e.target.value)}
              />
            </Grid>
          ))}
          <Grid item xs={12}>
            <Button variant="contained" color="primary" type="submit">
              Submit
            </Button>
          </Grid>
        </Grid>
      </form>
    </Container>
  );
};

export default AlgoParams;