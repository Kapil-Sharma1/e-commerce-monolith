import axios from 'axios'
import Cookie from 'js-cookie'

const config = {
  headers: {
    Authorization: Cookie.get( 'Authorization' ),
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'X-CSRFToken',
  },
}

const httpClient = axios.create( config )

httpClient.interceptors.response.use(
  ( response ) => response,
  ( error ) => {
    if (
      401 === error.response.status
      || ( 403 === error.response.status
        && 'Invalid token.' === error.response.data.detail )
    ) {
      delete httpClient.defaults?.headers['Authorization']
      Cookie.remove( 'Authorization' )

      const index = window.location.hostname.indexOf( '.' )
      const domain = window.location.hostname.slice( index )

      Cookie.remove( 'Authorization', {
        domain,
        path: '/',
      } )
    }
    return Promise.reject( error.response )
  },
)

export default httpClient
