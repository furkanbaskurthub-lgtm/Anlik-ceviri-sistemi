import React, { useState, useEffect } from "react";
import styled from "styled-components";
import { theme } from "../styles/theme";
import CallInterface from "./CallInterface";
import IncomingCallDialog from "./IncomingCallDialog";

const Container = styled.div`
  background-color: ${theme.colors.background};
  border-radius: ${theme.borderRadius.medium};
  box-shadow: ${theme.shadows.medium};
  width: 300px;
  height: 100%;
  display: flex;
  flex-direction: column;
`;

const Header = styled.div`
  background-color: ${theme.colors.primary};
  color: ${theme.colors.background};
  padding: ${theme.spacing.md};
  border-top-left-radius: ${theme.borderRadius.medium};
  border-top-right-radius: ${theme.borderRadius.medium};
  display: flex;
  justify-content: space-between;
  align-items: center;
`;

const Title = styled.h2`
  margin: 0;
  font-family: ${theme.fonts.primary};
  font-size: 1.2rem;
`;

const List = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: ${theme.spacing.md};
`;

const FriendItem = styled.div`
  display: flex;
  align-items: center;
  padding: ${theme.spacing.sm};
  margin-bottom: ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.small};
  background-color: ${theme.colors.background};
  transition: background-color 0.2s;

  &:hover {
    background-color: ${theme.colors.light};
  }
`;

const OnlineStatus = styled.div<{ isOnline: boolean }>`
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: ${(props) =>
    props.isOnline ? theme.colors.success : theme.colors.textLight};
  margin-right: ${theme.spacing.sm};
`;

const Username = styled.span`
  font-family: ${theme.fonts.primary};
  color: ${theme.colors.text};
  flex: 1;
`;

const LastSeen = styled.span`
  font-family: ${theme.fonts.primary};
  color: ${theme.colors.textLight};
  font-size: 0.8rem;
  margin-right: ${theme.spacing.sm};
`;

const ActionButton = styled.button`
  background-color: ${theme.colors.secondary};
  color: ${theme.colors.background};
  border: none;
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  border-radius: ${theme.borderRadius.small};
  cursor: pointer;
  font-family: ${theme.fonts.primary};
  transition: background-color 0.2s;

  &:hover {
    background-color: ${theme.colors.dark};
  }
`;

const CallButton = styled.button`
  background-color: ${theme.colors.success};
  color: ${theme.colors.background};
  border: none;
  padding: ${theme.spacing.xs} ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.small};
  cursor: pointer;
  opacity: 0.8;
  transition: opacity 0.2s;

  &:hover {
    opacity: 1;
  }

  &:disabled {
    background-color: ${theme.colors.textLight};
    cursor: not-allowed;
  }
`;

const RequestsBadge = styled.span`
  background-color: ${theme.colors.error};
  color: ${theme.colors.background};
  border-radius: 50%;
  padding: 2px 6px;
  font-size: 0.8rem;
  margin-left: ${theme.spacing.xs};
`;

const Notification = styled.div<{ type: 'error' | 'info' }>`
  position: fixed;
  top: 20px;
  right: 20px;
  background-color: ${props => props.type === 'error' ? theme.colors.error : theme.colors.primary};
  color: ${theme.colors.background};
  padding: ${theme.spacing.md};
  border-radius: ${theme.borderRadius.medium};
  box-shadow: ${theme.shadows.large};
  z-index: 2000;
  animation: slideIn 0.3s ease-out;
  
  @keyframes slideIn {
    from {
      transform: translateX(400px);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
`;

interface Friend {
  username: string;
  online_status: boolean;
  last_seen: string;
}

interface FriendsListProps {
  friends: Friend[];
  currentUsername: string;
  socket: any;
  onAddFriend: () => void;
  onShowRequests: () => void;
  pendingRequestsCount: number;
}

const FriendsList: React.FC<FriendsListProps> = ({
  friends,
  currentUsername,
  socket,
  onAddFriend,
  onShowRequests,
  pendingRequestsCount,
}) => {
  const [activeCall, setActiveCall] = useState<{username: string, isCaller: boolean, offer?: RTCSessionDescriptionInit} | null>(null);
  const [incomingCall, setIncomingCall] = useState<{
    username: string;
    offer: RTCSessionDescriptionInit;
  } | null>(null);
  const [notification, setNotification] = useState<{message: string, type: 'error' | 'info'} | null>(null);
  const [callTimeout, setCallTimeout] = useState<NodeJS.Timeout | null>(null);

  useEffect(() => {
    if (socket) {
      // Gelen çağrı
      socket.on(
        "incoming_call",
        (data: { caller: string; offer: RTCSessionDescriptionInit }) => {
          console.log('Incoming call from:', data.caller);
          setIncomingCall({
            username: data.caller,
            offer: data.offer,
          });
          
          // 30 saniye sonra otomatik reddet
          const timeout = setTimeout(() => {
            if (incomingCall?.username === data.caller) {
              handleRejectCall();
              showNotification('Çağrı zaman aşımına uğradı', 'info');
            }
          }, 30000);
          setCallTimeout(timeout);
        }
      );

      // Çağrı reddedildi
      socket.on("call_rejected", () => {
        console.log('Call rejected');
        showNotification('Çağrı reddedildi', 'error');
        handleEndCall();
      });

      // Çağrı sonlandı
      socket.on("call_ended", () => {
        console.log('Call ended');
        showNotification('Çağrı sonlandırıldı', 'info');
        handleEndCall();
      });

      // Hata durumu
      socket.on("error", (data: {message: string}) => {
        console.error('Socket error:', data.message);
        showNotification(data.message, 'error');
      });
    }
    
    return () => {
      if (socket) {
        socket.off("incoming_call");
        socket.off("call_rejected");
        socket.off("call_ended");
        socket.off("error");
      }
      if (callTimeout) {
        clearTimeout(callTimeout);
      }
    };
  }, [socket, incomingCall]);

  const showNotification = (message: string, type: 'error' | 'info') => {
    setNotification({message, type});
    setTimeout(() => setNotification(null), 3000);
  };

  const formatLastSeen = (dateString: string) => {
    if (!dateString) return "";
    const date = new Date(dateString);
    const now = new Date();
    const diffInMinutes = Math.floor((now.getTime() - date.getTime()) / 60000);

    if (diffInMinutes < 1) return "Az önce";
    if (diffInMinutes < 60) return `${diffInMinutes} dakika önce`;
    if (diffInMinutes < 1440) {
      const hours = Math.floor(diffInMinutes / 60);
      return `${hours} saat önce`;
    }
    return date.toLocaleDateString("tr-TR", {
      day: "numeric",
      month: "long",
      hour: "2-digit",
      minute: "2-digit",
    });
  };

  const handleCallFriend = (friendUsername: string) => {
    console.log('Calling friend:', friendUsername);
    setActiveCall({username: friendUsername, isCaller: true});
  };

  const handleEndCall = () => {
    console.log('Ending call');
    if (callTimeout) {
      clearTimeout(callTimeout);
      setCallTimeout(null);
    }
    setActiveCall(null);
    setIncomingCall(null);
  };

  const handleAcceptCall = () => {
    console.log('Accepting call from:', incomingCall?.username);
    if (incomingCall) {
      if (callTimeout) {
        clearTimeout(callTimeout);
        setCallTimeout(null);
      }
      setActiveCall({
        username: incomingCall.username, 
        isCaller: false,
        offer: incomingCall.offer
      });
      setIncomingCall(null);
    }
  };

  const handleRejectCall = () => {
    console.log('Rejecting call from:', incomingCall?.username);
    if (incomingCall && socket) {
      socket.emit("call_response", {
        caller: incomingCall.username,
        accepted: false,
      });
    }
    if (callTimeout) {
      clearTimeout(callTimeout);
      setCallTimeout(null);
    }
    setIncomingCall(null);
  };

  return (
    <>
      <Container>
        <Header>
          <Title>Arkadaşlar</Title>
          <div>
            <ActionButton onClick={onAddFriend}>Arkadaş Ekle</ActionButton>
            <ActionButton
              onClick={onShowRequests}
              style={{ marginLeft: theme.spacing.sm }}
            >
              İstekler
              {pendingRequestsCount > 0 && (
                <RequestsBadge>{pendingRequestsCount}</RequestsBadge>
              )}
            </ActionButton>
          </div>
        </Header>
        <List>
          {friends.map((friend) => (
            <FriendItem key={friend.username}>
              <OnlineStatus isOnline={friend.online_status} />
              <Username>{friend.username}</Username>
              {!friend.online_status && friend.last_seen && (
                <LastSeen>
                  Son görülme: {formatLastSeen(friend.last_seen)}
                </LastSeen>
              )}
              <CallButton
                onClick={() => handleCallFriend(friend.username)}
                disabled={!friend.online_status || activeCall !== null}
              >
                {activeCall?.username === friend.username ? 'Arıyor...' : 'Ara'}
              </CallButton>
            </FriendItem>
          ))}
          {friends.length === 0 && (
            <div
              style={{
                textAlign: "center",
                color: theme.colors.textLight,
                padding: theme.spacing.lg,
              }}
            >
              Henüz arkadaşınız yok
            </div>
          )}
        </List>
      </Container>

      {activeCall && (
        <CallInterface
          socket={socket}
          username={currentUsername}
          targetUser={activeCall.username}
          isCaller={activeCall.isCaller}
          incomingOffer={activeCall.offer}
          onClose={handleEndCall}
        />
      )}

      {incomingCall && !activeCall && (
        <IncomingCallDialog
          socket={socket}
          callerUsername={incomingCall.username}
          offer={incomingCall.offer}
          onAccept={handleAcceptCall}
          onReject={handleRejectCall}
        />
      )}

      {notification && (
        <Notification type={notification.type}>
          {notification.message}
        </Notification>
      )}
    </>
  );
};

export default FriendsList;
