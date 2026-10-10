import mysql from 'mysql2/promise';

export const pool = mysql.createPool({
    host: process.env.DB_HOST || 'localhost',
    port: Number(process.env.DB_PORT || 3306),
    user: process.env.DB_USER || 'root',
    password: process.env.DB_PASSWORD || '',
    database: process.env.DB_NAME || 'agrivision_x',
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0,
});

export async function testDatabaseConnection() {
    try {
        const connection = await pool.getConnection();

        console.log('MySQL database connected successfully');

        connection.release();
    } catch (error) {
        console.error('MySQL database connection failed:', error.message);
        throw error;
    }
}