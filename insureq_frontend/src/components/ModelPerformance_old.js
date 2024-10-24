import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Snackbar, MenuItem, Select, FormControl, InputLabel } from '@mui/material';

const ModelPerformance = () => {
    const [performances, setPerformances] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);
    const [selectedModel, setSelectedModel] = useState('RandomForest'); // Default model

    const fetchPerformances = async () => {
        setLoading(true);
        try {
            const response = await axios.get('http://localhost:8000/api/performance');
            setPerformances(response.data);
        } catch (error) {
            console.error("Error fetching performances:", error);
            setError("Failed to fetch performances.");
        } finally {
            setLoading(false);
        }
    };

    const calculateScores = async () => {
        try {
            // Sending request to the calculate performance endpoint
            const response = await axios.post('http://localhost:8000/api/performance/calculate');
            setSuccess(true);
            fetchPerformances(); // Fetch updated performances
        } catch (error) {
            console.error("Error calculating scores:", error);
            setError("Failed to create performance.");
        }
    };

    useEffect(() => {
        fetchPerformances();
    }, []);

    const handleCloseSnackbar = () => {
        setError('');
        setSuccess(false);
    };

    return (
        <Paper>
            <TableContainer>
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Model Name</TableCell>
                            <TableCell>Accuracy</TableCell>
                            <TableCell>Precision</TableCell>
                            <TableCell>Recall</TableCell>
                            <TableCell>F1 Score</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {performances.map((performance) => (
                            <TableRow key={performance.id}>
                                <TableCell>{performance.name}</TableCell>
                                <TableCell>{performance.accuracy}</TableCell>
                                <TableCell>{performance.precision}</TableCell>
                                <TableCell>{performance.recall}</TableCell>
                                <TableCell>{performance.f1_score}</TableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
            </TableContainer>
            <Button onClick={calculateScores} disabled={loading}>
                Calculate and Display Model Scores
            </Button>
            <Snackbar 
                open={Boolean(error)} 
                autoHideDuration={6000} 
                onClose={handleCloseSnackbar} 
                message={error} 
            />
            <Snackbar 
                open={success} 
                autoHideDuration={6000} 
                onClose={handleCloseSnackbar} 
                message="Performance created successfully!" 
            />
        </Paper>
    );
};

export default ModelPerformance;
