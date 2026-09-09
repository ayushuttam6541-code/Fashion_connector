import { Toaster as SonnerToaster } from 'sonner'

const Toaster = () => {
  return (
    <SonnerToaster
      position="top-center"
      richColors
      closeButton
      duration={4000}
    />
  )
}

export { Toaster }
