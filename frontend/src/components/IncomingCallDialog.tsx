import React from "react";
import styled from "styled-components";
import { theme } from "../styles/theme";
import { FaPhone, FaPhoneSlash } from "react-icons/fa";

interface IncomingCallDialogProps {
  socket: any;
  callerUsername: string;
  offer: RTCSessionDescriptionInit;
  onAccept: () => void;
  onReject: () => void;
}

const Container = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: ${theme.colors.background};
  border-radius: ${theme.borderRadius.medium};
  box-shadow: ${theme.shadows.large};
  padding: 30px;
  width: 350px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  z-index: 1500;
  animation: fadeIn 0.3s ease-out;
  
  @keyframes fadeIn {
    from {
      opacity: 0;
      transform: translate(-50%, -60%);
    }
    to {
      opacity: 1;
      transform: translate(-50%, -50%);
    }
  }
`;

const CallerAvatar = styled.div`
  width: 80px;
  height: 80px;
  border-radius: 50%;
  background: linear-gradient(135deg, ${theme.colors.primary}, ${theme.colors.secondary});
  display: flex;
  align-items: center;
  justify-content: center;
  color: ${theme.colors.background};
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 10px;
`;

const Title = styled.h3`
  margin: 0;
  color: ${theme.colors.text};
  text-align: center;
  font-size: 1.3rem;
`;

const Subtitle = styled.p`
  margin: 0;
  color: ${theme.colors.textLight};
  text-align: center;
  font-size: 0.9rem;
`;

const ButtonContainer = styled.div`
  display: flex;
  gap: 30px;
  margin-top: 10px;
`;

const Button = styled.button<{ isAccept?: boolean }>`
  width: 60px;
  height: 60px;
  border-radius: 50%;
  border: none;
  background-color: ${(props) =>
    props.isAccept ? theme.colors.success : theme.colors.error};
  color: white;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-size: 24px;
  box-shadow: ${theme.shadows.medium};

  &:hover {
    transform: scale(1.1);
    box-shadow: ${theme.shadows.large};
  }
  
  &:active {
    transform: scale(0.95);
  }
`;

const Overlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  z-index: 1400;
`;

const IncomingCallDialog: React.FC<IncomingCallDialogProps> = ({
  socket,
  callerUsername,
  offer,
  onAccept,
  onReject,
}) => {
  const getInitial = (name: string) => {
    return name.charAt(0).toUpperCase();
  };

  return (
    <>
      <Overlay onClick={onReject} />
      <Container>
        <CallerAvatar>{getInitial(callerUsername)}</CallerAvatar>
        <Title>{callerUsername}</Title>
        <Subtitle>Sizi arıyor...</Subtitle>
        <ButtonContainer>
          <Button onClick={onReject} title="Reddet">
            <FaPhoneSlash />
          </Button>
          <Button isAccept onClick={onAccept} title="Kabul Et">
            <FaPhone />
          </Button>
        </ButtonContainer>
      </Container>
    </>
  );
};

export default IncomingCallDialog;
