import React from 'react';
import { TextField } from '@mui/material';

const InputParamField = ({ name, value, onChange }) => {
  const handleChange = (event) => {
    onChange(name, event.target.value);
  };

  return (
    <div>
      <p>{name}</p>
      <p>{value}</p>
      <br />
      <TextField
        variant="outlined"
        margin="normal"
        sx={{ marginTop: 0 }}
        onChange={handleChange}
        value={value}
      />
    </div>
  );
};

export default InputParamField;