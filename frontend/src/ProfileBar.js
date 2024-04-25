import Logo from './Logo'; // Import the Logo component
import { Box, Typography } from '@mui/material';

ProfileBar.propTypes = {};

function ProfileBar(props) {
  return (
    <Box
      height={'55px'}
      sx={{
        margin: '10px',
        width: '100%',
        display: 'inline-flex',
        backgroundColor: '#ADD8E6',
        alignItems: 'center',
        position: 'absolute',
      }}
    >
      <Logo />
      <Typography level="h1">
        <strong>PACS CHAT</strong>
      </Typography>
      <Box />
    </Box>
  );
}

export default ProfileBar;
