import React, { useState, useEffect } from "react";
import axios from 'axios';
import api from "../api";
import Note from "../components/Note"
import "../styles/Home.css"
import "../styles/ProgressBar.css"
import isrcImage from "../images/isrc.jpg";
import Progressbar from "../components/ProgressBar";
import CustomDialog from "../components/CustomDialog";
import casnetImage from "../images/created_image.jpg";
import createdVideo from "../images/created_video.mp4";

function Home() {
    const [notes, setNotes] = useState([]);
    const [content, setContent] = useState("");
    const [selectedImage, setSelectedImage] = useState(null);
    const [selectedOption, setSelectedOption] = useState("");
    const [showDialog, setShowDialog] = useState(false);
    const [imageName, setImageName] = useState("");
    const [outputImage, setOutputImage] = useState(null); 
    const [outputVideo, setOutputVideo] = useState(null);
    const [showEmptyContainer, setShowEmptyContainer] = useState(false);
    const [videoUrl, setVideoUrl] = useState(null);
    const [backendEnd, setbackendEnd] = useState(false);
    const [isRunning, setIsRunning] = useState(false);
    const [authors, setAuthors] = useState([]);
    const [username, setUsername] = useState('');
    
    useEffect(() => {
        getNotes();
    }, []);

    //Get notes from database
    const getNotes = () => {
        api
            .get("/api/notes/")
            .then((res) => res.data)
            .then((data) => {
                setNotes(data);
                const authorsList = data.map(note => note.author);
                setAuthors(authorsList);
            })
            .catch((err) => alert(err));
        
    };

    //Delete notes related to images
    const deleteNote = (id) => {
        api
            .delete(`/api/notes/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("Nota apagada!");
                else alert("Falha ao apagar nota.");
                getNotes();
            })
            .catch((error) => alert(error));
    };

    //Create notes related to images
    const createNote = (e) => {
        e.preventDefault();
        api
            .post("/api/notes/", { content, imageURL: selectedImage.name, model: selectedOption })
            .then((res) => {
                if (res.status === 201) alert("Nota criada!");
                else alert("Falha ao criar a nota.");
                getNotes();
            })
            .catch((err) => alert(err));
    };

    //Handling image upload from the user's computer
    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        setSelectedImage(file);
        setVideoUrl(null); 
    };

    //Handling video upload from the user's computer
    const handleVideoUpload = (event) => {
        const file = event.target.files[0];
        if (file) {
            const videoUrl = URL.createObjectURL(file);
            setVideoUrl(videoUrl); // Update the state with the video URL
            setSelectedImage(null);
        }
    };

     //Handling method choice from user
    const handleOptionChange = (e) => {
        setSelectedOption(e.target.value);
    };

    //Confirming user's option
    const handlePrintInfo = () => {
        
        if (!selectedImage && !videoUrl) {
            alert("Por favor selecione uma imagem ou um video.");
            return;
        }
        if (!selectedOption) {
            alert("Por favor selecione um método.");
            return;
        }

        setShowDialog(true);
    };

    //Sending chosen image or video to the backend for processing
    const handleShowMedia = async () => {
        setShowEmptyContainer(true);
        setIsRunning(false);
        let step = 1;
        
        try {
            const formData = new FormData();
            if (selectedImage) {
                formData.append('image', selectedImage);
                step = 9.9;
            } else if (videoUrl) {
                const response = await fetch(videoUrl);
                const blob = await response.blob();
                formData.append('video', new File([blob], 'video.mp4', { type: 'video/mp4' }));
                step =1;
            }
            formData.append('option', selectedOption);
            formData.append('user', authors[0]);
            setIsRunning(true);

            const endpoint = selectedImage ? 'process-image' : 'process-video';

            const response = await axios.post(`http://localhost:8000/process/${endpoint}/`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data'
                }
            });
            
            if (response.status === 200){
                setbackendEnd(true);
                setIsRunning(false);
            }
        } catch (error) {
            console.error('Error uploading the media:', error);
            setOutputImage(null);
            setOutputVideo(null);
            setIsRunning(false);
        }
    };

    //closing show dialog popup box
    const handleCloseDialog = () => {
        setShowDialog(false);
      };
    
    //Show the correct image to the user, depending on the model chosen
    useEffect(() => {
        const imageName = selectedImage && selectedOption ? `${selectedImage.name.split('.')[0]}${selectedOption}.jpg` : "";
        setImageName(imageName);
    
        if (backendEnd) {
            if (imageName) {
                setOutputImage(casnetImage);
                setOutputVideo(null);
            } else if (videoUrl) {
                setOutputVideo(createdVideo);
                setOutputImage(null);
            }
        } else {
            setOutputImage(null);
            setOutputVideo(null);
        }
        
        
    }, [backendEnd, selectedOption, videoUrl]);

    return (
        <div>
            <div className="center">
                <img src={isrcImage} alt="ISRC logo" ></img>
            </div>
            
            <div style={{ textAlign: "right" }}>
                <a href="http://localhost:5173/logout">Logout</a>
            </div>

            <div style={{ textAlign: "center" }}>
                <br></br>
                <label htmlFor="image" style={{ display: "block", textAlign: "center" }}>Escolha uma imagem ou um video para a criação do mapa de saliências:</label>
                <input 
                    type="file" 
                    id="imageInput" 
                    style={{ margin: "0 auto", display: "none" }} 
                    onChange={handleImageUpload} 
                    accept="image/*" />
                <button onClick={() => document.getElementById("imageInput").click()} >Escolher Imagem</button> {}
                <input
                    type="file"
                    id="videoInput"
                    style={{ margin: "0 auto", display: "none" }}
                    onChange={handleVideoUpload}
                    accept="video/*" // Only accept video files
                />
                <button type="button" onClick={() => document.getElementById("videoInput").click()}>Escolher Vídeo</button>
            </div>
            
            <div className="break"></div>

            <div className="centered-container combo-box-container">
                <label htmlFor="casnet" style={{ display: "block", textAlign: "center" }}>Escolha um modelo para a criação do mapa de saliências:</label>
                <select id="casnet" name="casnet" onChange={handleOptionChange} value={selectedOption} style={{ margin: "0 auto", display: "block" }}>
                    <option value="">Selecione um modelo...</option>
                    <option value="casnet1">CASNET 1</option>
                    <option value="casnet2">CASNET 2</option>
                </select>
            </div>
            
            <div className="break"></div>

            <div id="imageContainer" className="container">
                {selectedImage && (
                    <img src={URL.createObjectURL(selectedImage)} alt="Selected Image" style={{ maxWidth: "100%" }} />
                )}
                {videoUrl && (
                    <video controls style={{ maxWidth: "100%" }}>
                        <source src={videoUrl} type="video/mp4" />
                    </video>
                )}
            </div>

            <div id="emptyContainer" className="container">
                {outputImage && showEmptyContainer && (
                    <img src={casnetImage} alt="Output Image" style={{ maxWidth: "100%" }} />
                )}
                {outputVideo && showEmptyContainer && (
                    <video controls style={{ maxWidth: "100%" }}>
                        <source src={outputVideo} type="video/mp4" />
                    </video>
                )}
            </div>
            
            <div className="break"></div> 
            
            <div className="ProgressBar">
                    <Progressbar isRunning={isRunning} step={selectedImage ? 9.9 : 1}/>
            </div>
            
            <div className="break"></div> 

            <div style={{ textAlign: "center", marginTop: "20px" }}>
                <button onClick={handlePrintInfo} style={{ width: "50%" }}>Criar mapa de saliências</button>
            </div>

            <div style={{ borderBottom: "4px solid black", margin: "20px auto", width: "90%" }}></div>
            
            <div>
                <h2>Notas</h2>
                {notes.map((note) => (
                    <Note note={note} onDelete={deleteNote} key={note.id} />
                ))}
            </div>
            <h2>Criar uma Nota</h2>
            <form onSubmit={createNote}>
                <label htmlFor="content">Conteudo:</label>
                <br />
                <textarea
                    id="content"
                    name="content"
                    required
                    value={content}
                    onChange={(e) => setContent(e.target.value)}
                ></textarea>
                <br />
                <input type="submit" value="Submit"></input>
            </form>
            
            <div style={{ borderBottom: "4px solid black", margin: "20px auto", width: "90%" }}></div>

                <h2 className="centered-text">Página desenvolvida por: Pedro Santos - 1200690@isep.ipp.pt</h2>

            
            {showDialog && (
                <CustomDialog
                message={`Tem a certeza que pretende criar o mapa de saliências?`}
                onClose={handleCloseDialog}
                onShowImage={handleShowMedia}
                showEmptyContainer={showEmptyContainer}
                />
            )}
        </div>
    );
}

export default Home;