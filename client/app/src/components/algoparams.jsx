import React, { useState } from 'react';
import { Checkbox, Container, FormControlLabel } from '@mui/material';
import InputParamField from './inputparamfiled';

const AlgoParams = ({ parameters, values, onChangeParam }) => {
  // Обработчик изменений значения параметра
  const handleChange = (parameterName, value) => {
    onChangeParam(parameterName, value);
  };

  return (
    <Container sx={{ marginLeft: 0, paddingLeft: 0, border: "1px solid"}}>
    {
        parameters && parameters.map((parameter, index) => (
        <InputParamField
            key={index}
            name={parameter}
            value={values[parameter]}
            onChange={handleChange}
        />
        ))
    }
    <FormControlLabel control={<Checkbox />} label="Нужен график" />
    <br/>
    <FormControlLabel control={<Checkbox />} label="Обучение на всей обучающей выборке" />
    </Container>

  );
};

export default AlgoParams;
