import React from 'react'
import { useFormContext } from 'react-hook-form'

const FormLabel = ( { children, name, field, className, required } ) => {
  const { formState } = useFormContext() || { formState: null }

  return (
    <label
      htmlFor={ name }
      className={ `form-label ${ className } ${ required && 'required' }` }
    >
      <span className={ formState?.errors[name] && 'error' }>{field}</span>
      {children}
      <span className='helper-text error'>
        {formState?.errors[name]?.message}
      </span>
    </label>
  )
}

export default FormLabel
