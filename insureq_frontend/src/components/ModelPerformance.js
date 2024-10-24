import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Button, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, Snackbar } from '@mui/material';
import { Bar } from 'react-chartjs-2';
import {
    Chart as ChartJS,
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
} from 'chart.js';

ChartJS.register(
    CategoryScale,
    LinearScale,
    BarElement,
    Title,
    Tooltip,
    Legend
);

const ModelPerformance = () => {
    const [performances, setPerformances] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');
    const [success, setSuccess] = useState(false);

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
            await axios.post('http://localhost:8000/api/performance/calculate');
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

    // Prepare data for the bar chart
    const chartData = {
        labels: performances.map(performance => performance.name),
        datasets: [
            {
                label: 'Accuracy',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1,
                data: performances.map(performance => performance.accuracy),
            },
            {
                label: 'Precision',
                backgroundColor: 'rgba(54, 162, 235, 0.2)',
                borderColor: 'rgba(54, 162, 235, 1)',
                borderWidth: 1,
                data: performances.map(performance => performance.precision),
            },
            {
                label: 'Recall',
                backgroundColor: 'rgba(255, 206, 86, 0.2)',
                borderColor: 'rgba(255, 206, 86, 1)',
                borderWidth: 1,
                data: performances.map(performance => performance.recall),
            },
            {
                label: 'F1 Score',
                backgroundColor: 'rgba(153, 102, 255, 0.2)',
                borderColor: 'rgba(153, 102, 255, 1)',
                borderWidth: 1,
                data: performances.map(performance => performance.f1_score),
            },
        ],
    };

    const chartOptions = {
        responsive: true,
        maintainAspectRatio: false, 
        plugins: {
            legend: {
                position: 'top',
            },
            title: {
                display: true,
                text: 'Model Performance Metrics',
            },
        },
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
            <div style={{ width: '100%', height: "400px", marginTop: '20px' }}>
                <Bar data={chartData} options={chartOptions} />
            </div>

        </Paper>
    );
};

export default ModelPerformance;
