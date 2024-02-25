import { useMutation, useQueryClient } from 'react-query'
import httpClient from './httpClient'

const Patch = ( endpoint, params ) => {
  const queryClient = useQueryClient()

  const patchQueryFunction = ( mutateData ) =>
    new Promise( ( resolve, reject ) => {
      const updateUid = params?.updateUid

      const _endpoint = !!updateUid ? `${ endpoint }/${ updateUid }` : endpoint

      httpClient
        .patch( `${ _endpoint }/`, { ...mutateData } )
        .then( ( { data } ) => {
          resolve( data )
        } )
        .catch( ( e ) => {
          reject( e )
        } )
    } )

  return useMutation( patchQueryFunction, {
    // Refetch data after mutation
    onSettled: () => {
      queryClient.invalidateQueries( endpoint )
    },
  } )
}

export default Patch
