import React from 'react';
import { TextField } from '@mui/material';
import { algoParamsRus } from '../config';

const InputParamField = ({ name, value, onChange }) => {
  const handleChange = (event) => {
    onChange(name, event.target.value);
  };

  return (
    <div>
      <p>{algoParamsRus[name]}</p>
      <TextField
        variant="outlined"
        margin="normal"
        sx={{ marginTop: 0}}
        onChange={handleChange}
        value={value}
        size="small"
      />
    </div>
  );
};

export default InputParamField;