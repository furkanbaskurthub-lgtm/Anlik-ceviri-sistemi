import React, { useEffect, useRef, useState } from "react";
import styled from "styled-components";
import { theme } from "../styles/theme";
import {
  FaMicrophone,
  FaMicrophoneSlash,
  FaVideo,
  FaVideoSlash,
  FaPhoneSlash,
  FaLanguage,
} from "react-icons/fa";

interface CallInterfaceProps {
  socket: any;
  username: string;
  targetUser: string;
  isCaller: boolean;
  incomingOffer?: RTCSessionDescriptionInit;
  onClose: () => void;
}

const Container = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background-color: ${theme.colors.background};
  border-radius: ${theme.borderRadius.medium};
  box-shadow: ${theme.shadows.large};
  padding: ${theme.spacing.lg};
  width: 80%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  align-items: center;
`;

const VideoContainer = styled.div`
  display: flex;
  gap: ${theme.spacing.lg};
  margin-bottom: ${theme.spacing.lg};
  width: 100%;
`;

const VideoWrapper = styled.div`
  flex: 1;
  position: relative;
`;

const Video = styled.video`
  width: 100%;
  border-radius: ${theme.borderRadius.medium};
  background-color: ${theme.colors.dark};
`;

const Username = styled.div`
  position: absolute;
  bottom: ${theme.spacing.sm};
  left: ${theme.spacing.sm};
  background-color: rgba(0, 0, 0, 0.5);
  color: ${theme.colors.background};
  padding: ${theme.spacing.xs} ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.small};
  font-family: ${theme.fonts.primary};
`;

const Controls = styled.div`
  display: flex;
  gap: ${theme.spacing.md};
  align-items: center;
`;

const LanguageSelector = styled.div`
  display: flex;
  gap: ${theme.spacing.sm};
  align-items: center;
  background-color: ${theme.colors.dark};
  padding: ${theme.spacing.sm} ${theme.spacing.md};
  border-radius: ${theme.borderRadius.medium};
  color: ${theme.colors.background};
`;

const Select = styled.select`
  background-color: ${theme.colors.background};
  color: ${theme.colors.dark};
  border: none;
  padding: ${theme.spacing.xs} ${theme.spacing.sm};
  border-radius: ${theme.borderRadius.small};
  font-family: ${theme.fonts.primary};
  cursor: pointer;
  
  &:focus {
    outline: 2px solid ${theme.colors.primary};
  }
`;

const TranslationStatus = styled.div`
  margin-top: ${theme.spacing.md};
  padding: ${theme.spacing.md};
  background-color: rgba(0, 0, 0, 0.05);
  border-radius: ${theme.borderRadius.medium};
  max-height: 150px;
  overflow-y: auto;
`;

const TranslationText = styled.div<{ isOriginal?: boolean }>`
  margin-bottom: ${theme.spacing.sm};
  padding: ${theme.spacing.xs};
  font-size: 14px;
  color: ${(props) => (props.isOriginal ? theme.colors.dark : theme.colors.primary)};
  font-style: ${(props) => (props.isOriginal ? "normal" : "italic")};
`;

const ControlButton = styled.button<{ isActive?: boolean; isEnd?: boolean }>`
  background-color: ${(props) =>
    props.isEnd
      ? theme.colors.error
      : props.isActive
      ? theme.colors.success
      : theme.colors.dark};
  color: ${theme.colors.background};
  border: none;
  border-radius: 50%;
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background-color 0.2s;

  &:hover {
    opacity: 0.8;
  }
`;

const CallInterface: React.FC<CallInterfaceProps> = ({
  socket,
  username,
  targetUser,
  isCaller,
  incomingOffer,
  onClose,
}) => {
  const [localStream, setLocalStream] = useState<MediaStream | null>(null);
  const [remoteStream, setRemoteStream] = useState<MediaStream | null>(null);
  const [isAudioEnabled, setIsAudioEnabled] = useState(true);
  const [isVideoEnabled, setIsVideoEnabled] = useState(true);
  const [sourceLanguage, setSourceLanguage] = useState("tr");
  const [targetLanguage, setTargetLanguage] = useState("en");
  const [translations, setTranslations] = useState<Array<{original: string, translated: string}>>([]);
  const [isTranslationEnabled, setIsTranslationEnabled] = useState(true);
  
  const peerConnection = useRef<RTCPeerConnection | null>(null);
  const localVideoRef = useRef<HTMLVideoElement>(null);
  const remoteVideoRef = useRef<HTMLVideoElement>(null);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const audioChunksRef = useRef<Blob[]>([]);

  useEffect(() => {
    const initializeCall = async () => {
      try {
        // Get user media
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true,
        });
        setLocalStream(stream);

        if (localVideoRef.current) {
          localVideoRef.current.srcObject = stream;
        }

        // Initialize audio recording for translation
        startAudioRecording(stream);

        // Create peer connection
        const pc = new RTCPeerConnection({
          iceServers: [
            { urls: "stun:stun.l.google.com:19302" },
            { urls: "stun:stun1.l.google.com:19302" }
          ],
        });
        peerConnection.current = pc;

        // Add local stream to peer connection
        stream.getTracks().forEach((track) => {
          pc.addTrack(track, stream);
        });

        // Handle incoming tracks
        pc.ontrack = (event) => {
          console.log('Received remote track');
          setRemoteStream(event.streams[0]);
          if (remoteVideoRef.current) {
            remoteVideoRef.current.srcObject = event.streams[0];
          }
        };

        // Handle ICE candidates
        pc.onicecandidate = (event) => {
          if (event.candidate) {
            console.log('Sending ICE candidate');
            socket.emit("ice_candidate", {
              target: targetUser,
              candidate: event.candidate,
            });
          }
        };

        // Handle connection state changes
        pc.onconnectionstatechange = () => {
          console.log('Connection state:', pc.connectionState);
          if (pc.connectionState === 'failed' || pc.connectionState === 'disconnected') {
            console.error('Connection failed or disconnected');
            onClose();
          }
        };

        if (isCaller) {
          // Caller: Create and send offer
          console.log('Creating offer as caller');
          const offer = await pc.createOffer({
            offerToReceiveAudio: true,
            offerToReceiveVideo: true
          });
          await pc.setLocalDescription(offer);
          socket.emit("call_user", {
            caller: username,
            callee: targetUser,
            offer: offer,
          });
        } else if (incomingOffer) {
          // Callee: Set remote description and create answer
          console.log('Creating answer as callee');
          await pc.setRemoteDescription(new RTCSessionDescription(incomingOffer));
          const answer = await pc.createAnswer();
          await pc.setLocalDescription(answer);
          socket.emit("call_response", {
            caller: targetUser,
            accepted: true,
            answer: answer,
          });
        }
      } catch (error: any) {
        console.error("Error initializing call:", error);
        
        let errorMessage = 'Çağrı başlatılamadı.';
        
        if (error.name === 'NotAllowedError') {
          errorMessage = 'Kamera ve mikrofon erişimi reddedildi. Lütfen tarayıcı ayarlarından izin verin.';
        } else if (error.name === 'NotFoundError') {
          errorMessage = 'Kamera veya mikrofon bulunamadı. Lütfen cihazlarınızı kontrol edin.';
        } else if (error.name === 'NotReadableError') {
          errorMessage = 'Kamera veya mikrofon başka bir uygulama tarafından kullanılıyor. Lütfen diğer uygulamaları kapatın.';
        } else if (error.name === 'OverconstrainedError') {
          errorMessage = 'Kamera veya mikrofon ayarları uygun değil.';
        } else if (error.name === 'AbortError') {
          errorMessage = 'Medya cihazlarına erişim iptal edildi.';
        }
        
        alert(errorMessage + '\n\nNot: Aynı bilgisayarda iki tarayıcı sekmesinde test yapıyorsanız, bu normal bir durumdur. Gerçek test için farklı cihazlar kullanın.');
        onClose();
      }
    };

    initializeCall();

    // Clean up
    return () => {
      console.log('Cleaning up call interface');
      if (localStream) {
        localStream.getTracks().forEach((track) => track.stop());
      }
      if (peerConnection.current) {
        peerConnection.current.close();
      }
      if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    };
  }, []);

  useEffect(() => {
    if (!socket) return;

    socket.on(
      "call_accepted",
      async (data: { answer: RTCSessionDescriptionInit }) => {
        if (peerConnection.current) {
          await peerConnection.current.setRemoteDescription(data.answer);
        }
      }
    );

    socket.on(
      "ice_candidate",
      async (data: { candidate: RTCIceCandidateInit }) => {
        if (peerConnection.current) {
          await peerConnection.current.addIceCandidate(data.candidate);
        }
      }
    );

    socket.on("call_rejected", () => {
      onClose();
    });

    socket.on("call_ended", () => {
      onClose();
    });

    // Handle incoming translated audio
    socket.on("translated_audio", (data: { audio: ArrayBuffer, original_text: string, translated_text: string }) => {
      // Add to translations display
      setTranslations(prev => [...prev, { original: data.original_text, translated: data.translated_text }].slice(-5));
      
      // Play translated audio
      const audioBlob = new Blob([data.audio], { type: 'audio/mp3' });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      audio.play().catch(err => console.error('Error playing translated audio:', err));
    });

    return () => {
      socket.off("call_accepted");
      socket.off("ice_candidate");
      socket.off("call_rejected");
      socket.off("call_ended");
      socket.off("translated_audio");
    };
  }, [socket]);

  const startAudioRecording = (stream: MediaStream) => {
    try {
      const audioTrack = stream.getAudioTracks()[0];
      const mediaStream = new MediaStream([audioTrack]);
      
      const mediaRecorder = new MediaRecorder(mediaStream, {
        mimeType: 'audio/webm;codecs=opus'
      });
      
      mediaRecorderRef.current = mediaRecorder;
      audioChunksRef.current = [];

      mediaRecorder.ondataavailable = async (event) => {
        if (event.data.size > 0 && isTranslationEnabled) {
          // Send audio chunk for translation
          const reader = new FileReader();
          reader.readAsArrayBuffer(event.data);
          reader.onloadend = () => {
            const arrayBuffer = reader.result as ArrayBuffer;
            socket.emit('real_time_audio', {
              target: targetUser,
              audio: arrayBuffer,
              source_language: sourceLanguage,
              target_language: targetLanguage
            });
          };
        }
      };

      // Record in 3-second chunks for real-time translation
      mediaRecorder.start();
      const recordInterval = setInterval(() => {
        if (mediaRecorder.state === 'recording') {
          mediaRecorder.stop();
          mediaRecorder.start();
        }
      }, 3000);

      // Store interval for cleanup
      (mediaRecorder as any).recordInterval = recordInterval;
      
    } catch (error) {
      console.error('Error starting audio recording:', error);
    }
  };

  const toggleAudio = () => {
    if (localStream) {
      const audioTrack = localStream.getAudioTracks()[0];
      audioTrack.enabled = !audioTrack.enabled;
      setIsAudioEnabled(audioTrack.enabled);
    }
  };

  const toggleVideo = () => {
    if (localStream) {
      const videoTrack = localStream.getVideoTracks()[0];
      videoTrack.enabled = !videoTrack.enabled;
      setIsVideoEnabled(videoTrack.enabled);
    }
  };

  const toggleTranslation = () => {
    setIsTranslationEnabled(!isTranslationEnabled);
  };

  const handleEndCall = () => {
    // Stop recording
    if (mediaRecorderRef.current) {
      if ((mediaRecorderRef.current as any).recordInterval) {
        clearInterval((mediaRecorderRef.current as any).recordInterval);
      }
      if (mediaRecorderRef.current.state !== 'inactive') {
        mediaRecorderRef.current.stop();
      }
    }
    
    socket.emit("end_call", { target: targetUser });
    onClose();
  };

  return (
    <Container>
      <VideoContainer>
        <VideoWrapper>
          <Video ref={localVideoRef} autoPlay muted playsInline />
          <Username>{username} (Sen)</Username>
        </VideoWrapper>
        <VideoWrapper>
          <Video ref={remoteVideoRef} autoPlay playsInline />
          <Username>{targetUser}</Username>
        </VideoWrapper>
      </VideoContainer>
      
      <LanguageSelector>
        <FaLanguage />
        <span>Konuştuğum Dil:</span>
        <Select value={sourceLanguage} onChange={(e) => setSourceLanguage(e.target.value)}>
          <option value="tr">Türkçe</option>
          <option value="en">English</option>
          <option value="es">Español</option>
          <option value="fr">Français</option>
          <option value="de">Deutsch</option>
          <option value="it">Italiano</option>
        </Select>
        <span>→</span>
        <span>Çevrilecek Dil:</span>
        <Select value={targetLanguage} onChange={(e) => setTargetLanguage(e.target.value)}>
          <option value="en">English</option>
          <option value="tr">Türkçe</option>
          <option value="es">Español</option>
          <option value="fr">Français</option>
          <option value="de">Deutsch</option>
          <option value="it">Italiano</option>
        </Select>
      </LanguageSelector>

      {translations.length > 0 && (
        <TranslationStatus>
          {translations.map((t, idx) => (
            <div key={idx}>
              <TranslationText isOriginal>{t.original}</TranslationText>
              <TranslationText>{t.translated}</TranslationText>
            </div>
          ))}
        </TranslationStatus>
      )}
      
      <Controls>
        <ControlButton onClick={toggleAudio} isActive={isAudioEnabled}>
          {isAudioEnabled ? <FaMicrophone /> : <FaMicrophoneSlash />}
        </ControlButton>
        <ControlButton onClick={toggleVideo} isActive={isVideoEnabled}>
          {isVideoEnabled ? <FaVideo /> : <FaVideoSlash />}
        </ControlButton>
        <ControlButton onClick={toggleTranslation} isActive={isTranslationEnabled}>
          <FaLanguage />
        </ControlButton>
        <ControlButton onClick={handleEndCall} isEnd>
          <FaPhoneSlash />
        </ControlButton>
      </Controls>
    </Container>
  );
};

export default CallInterface;
