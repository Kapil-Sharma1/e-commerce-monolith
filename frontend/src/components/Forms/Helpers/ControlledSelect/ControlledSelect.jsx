import React from 'react'
import { Controller, useFormContext } from 'react-hook-form'

import Select from '../../../Select'

const ControlledSelect = ( {
  name,
  label,
  labelField,
  placeholder,
  defaultOptions,
  keyField,
  valueField = 'value',
  rules = {},
} ) => {
  const { setValue, trigger, formState } = useFormContext()

  const handleChange = ( option ) => {
    setValue( name, option[valueField] )
    trigger( name )
  }

  return (
    <Controller
      name={ name }
      rules={ rules }
      render={ ( { field: { onChange, onBlur, value } } ) => (
        <Select
          name={ name }
          defaultOptions={ defaultOptions }
          label={ label }
          labelField={ labelField }
          valueField={ valueField }
          hasError={ !!formState.errors?.[name] }
          onBlur={ onBlur }
          onChange={ onChange }
          onSelect={ handleChange }
          placeholder={ placeholder ?? label }
          defaultValue={ value }
          keyField={ keyField ?? valueField }
        />
      ) }
    />
  )
}

export default ControlledSelect
