import React, { useRef, useState, useEffect } from "react";
import { Button, FormLabel } from '@mui/material';
import Box from '@mui/material/Box';
import TextField from '@mui/material/TextField';

const serverAddr = process.env.SERVER_ADDR || "localhost";
const serverPort = process.env.SERVER_PORT || 8000;



const defaultValues = {
    depth: 3,
    soln_size: 5,
    initial_state_file: 1,
    gamma: 0.95,
    threshold: 0.5,
    sched_threshold: 0.5,
    k: 1,
    beam_width: 5250,
    max_checks: 10,
}

const ImageWrapper = (data) => <img src={`data:image/jpeg;base64,${data}`} />


export const MainView = () => {

    const [formValues, setFormValues] = useState(defaultValues)
    const [resultText, setResultText] = useState("")
    const [img1, setImg1] = useState(null)
    const [img2, setImg2] = useState(null)
    const [img3, setImg3] = useState(null)
    const [img4, setImg4] = useState(null)
    const [img5, setImg5] = useState(null)


    const handleInputChange = (e) => {
        console.log(e.target)
        const { id, value } = e.target;
        setFormValues({
            ...formValues,
            [id]: value,
        });
    }

    const run = () => {
        const url = `http://${serverAddr}:${serverPort}/run?depth=${formValues.depth}&soln_size=${formValues.soln_size}&initial_state_file=${formValues.initial_state_file}&gamma=${formValues.gamma}&threshold=${formValues.threshold}&sched_threshold=${formValues.sched_threshold}&k=${formValues.k}&beam_width=${formValues.beam_width}&max_checks=${formValues.max_checks}`;
        fetch(url, {
            method: "GET",
        })
            .then(res => res.json())
            .then(json => {
                // console.log(json.text)
                // console.log(json.image1)     
                // setResultText(json.text)
                setImg1(json.image1)
                setImg2(json.image2)
                setImg3(json.image3)
                setImg4(json.image4)
                setImg5(json.image5)
            })

    }

    const clear = () => {
        const url = `http://${serverAddr}:${serverPort}/clear`
        fetch(url, {
            method: "POST",
        })
        setImg1(null)
        setImg2(null)
        setImg3(null)
        setImg4(null)
        setImg5(null)

    }
    const reset = () => {
        const url = `http://${serverAddr}:${serverPort}/reset`
        fetch(url, {
            method: "POST",
        })
    }

    return (
        <div>
            <Box
                component="form"
                sx={{
                    '& > :not(style)': { m: 1, width: '25ch' },
                }}
                noValidate
                autoComplete="off"
            >
                <TextField id="depth"
                    label="depth"
                    variant="outlined"
                    type="text"
                    value={formValues.depth}
                    onChange={e => handleInputChange(e)} />

                <TextField id="soln_size"
                    label="soln_size"
                    variant="outlined"
                    type="text"
                    value={formValues.soln_size}
                    onChange={e => handleInputChange(e)} />

                <TextField id="initial_state_file"
                    label="initial_state_file"
                    variant="outlined"
                    type="text"
                    value={formValues.initial_state_file}
                    onChange={e => handleInputChange(e)} />


                <TextField id="gamma"
                    label="gamma"
                    variant="outlined"
                    type="text"
                    value={formValues.gamma}
                    onChange={e => handleInputChange(e)} />

                <TextField id="threshold"
                    label="threshold"
                    variant="outlined"
                    type="text"
                    value={formValues.threshold}
                    onChange={e => handleInputChange(e)} />

                <TextField id="sched_threshold"
                    label="sched_threshold"
                    variant="outlined"
                    type="text"
                    value={formValues.sched_threshold}
                    onChange={e => handleInputChange(e)} />

                <TextField id="k"
                    label="k"
                    variant="outlined"
                    type="text"
                    value={formValues.k}
                    onChange={e => handleInputChange(e)} />


                <TextField id="beam_width"
                    label="beam_width"
                    variant="outlined"
                    type="text"
                    value={formValues.beam_width}
                    onChange={e => handleInputChange(e)} />

                <TextField id="max_checks"
                    label="max_checks"
                    variant="outlined"
                    type="text"
                    value={formValues.max_checks}
                    onChange={e => handleInputChange(e)} />


                <Button onClick={run}>Run</Button>
                <Button onClick={clear}>Clear</Button>
                <Button onClick={reset}>Reset</Button>


            </Box>

            <div>
                {resultText}
                <img src={`data:image/jpeg;base64,${img1}`} width="1200" height="700" />
                <img src={`data:image/jpeg;base64,${img2}`} width="1200" height="700" />
                <img src={`data:image/jpeg;base64,${img3}`} width="1200" height="700" />
                <img src={`data:image/jpeg;base64,${img4}`} width="1200" height="700" />
                <img src={`data:image/jpeg;base64,${img5}`} width="1200" height="700" />
            </div>
        </div >
    );
}