import React, { useContext } from 'react'

import Form from '../../../components/Forms/Form/Form'
import LoginForm from '../../../components/Forms/LoginForm'
import AuthContext from '../../../common/auth'

const Login = ( { goToSuccessPage, goToForgotPassword } ) => {
  const { setUserData } = useContext( AuthContext )

  const onSuccess = ( responseData ) => {
    setUserData( { loginAttempt: responseData } )
    goToSuccessPage()
  }

  return (
    <div>
      <h3>Welcome to The Alinea Group’s secure data application.</h3>

      <p>Please sign in below to access the system</p>

      <Form
        method='post'
        endpoint='/api/auth/login'
        onSuccess={ onSuccess }
        showOnlyToastErrors={ true }
        FormBody={ ( props ) =>
          LoginForm( {
            ...props,
            goToForgotPassword,
          } )
        }
      />
    </div>
  )
}

export default Login
