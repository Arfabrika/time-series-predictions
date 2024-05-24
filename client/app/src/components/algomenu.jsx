import React, { useState } from 'react';
import { FormControlLabel, Checkbox, TextField, Grid, Container, MenuList, MenuItem } from '@mui/material';

const AlgoMenu = ({selectedAlgorithms, setSelectedAlgorithms}) => {
    return (
    <div>
       <MenuList>
        {Object.keys(selectedAlgorithms).map(key => (
            <MenuItem>
                {key} | {selectedAlgorithms[key].toString()}
            </MenuItem>
        ))}
       </MenuList>
    </div>
  );
};

export default AlgoMenu;
