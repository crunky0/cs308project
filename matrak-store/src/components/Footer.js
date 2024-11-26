import React from 'react';

function Footer() {
  return (
    <footer style={footerStyle}>
      <p>© Group 33 Matrak Store. All rights reserved.</p>
    </footer>
  );
}

const footerStyle = {
  background: '#282c34',
  color: 'white',
  textAlign: 'center',
  padding: '10px 0',
  position: 'absolute',
  bottom: '0',
  width: '100%',
};

export default Footer;
