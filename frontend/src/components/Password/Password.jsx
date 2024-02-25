import React, { forwardRef, useState } from 'react'
import { useFormContext } from 'react-hook-form'
import classNames from 'classnames'

import './Password.scss'

import Icon from '../Icon'
import {
  ShowIcon as ShowPasswordIcon,
  HideIcon as HidePasswordIcon,
} from '../../assets/icons'
import FormLabel from '../Forms/Helpers/FormLabel'

const Password = (
  { placeholder, field = 'Password', name = 'password', isRequired = true },
  ref,
) => {
  const { register, formState } = useFormContext()

  const [ showPassword, setShowPassword ] = useState( false )

  const toggle = () => {
    setShowPassword( !showPassword )
  }

  return (
    <FormLabel name={ name } field={ field } required={ isRequired }>
      <div className='password-field-container'>
        <input
          className={ classNames( {
            error: formState?.errors[name],
            'full-width': true,
          } ) }
          type={ showPassword ? 'text' : 'password' }
          { ...register( name, { required: isRequired && 'This field is required' } ) }
          placeholder={ placeholder ?? field }
        />
        {!showPassword ? (
          <Icon
            className='right-inline-icon dark md'
            IconComponent={ ShowPasswordIcon }
            onClick={ toggle }
            fill='grey'
          />
        ) : (
          <Icon
            className='right-inline-icon dark md'
            IconComponent={ HidePasswordIcon }
            onClick={ toggle }
            fill='grey'
          />
        )}
      </div>
    </FormLabel>
  )
}

export default forwardRef( Password )
