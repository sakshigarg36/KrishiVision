import { pool } from '../config/db.js';
import bcrypt from 'bcryptjs';
import jwt from 'jsonwebtoken';

function generateToken(user) {
    return jwt.sign(
        {
            id: user.id,
            email: user.email
        },
        process.env.JWT_SECRET,
        {
            expiresIn: '7d'
        }
    );
}

export async function register(req, res, next) {
    try {
        const { name, email, password } = req.body;

        if (!name || !email || !password) {
            return res.status(400).json({
                error: 'name, email and password are required'
            });
        }

        if (password.length < 6) {
            return res.status(400).json({
                error: 'Password must be at least 6 characters'
            });
        }

        const [existingUsers] = await pool.execute(
            'SELECT id FROM users WHERE email = ?',
            [email]
        );

        if (existingUsers.length > 0) {
            return res.status(409).json({
                error: 'Email already registered'
            });
        }

        const passwordHash = await bcrypt.hash(password, 10);

        const [result] = await pool.execute(
            `INSERT INTO users (name, email, password_hash)
             VALUES (?, ?, ?)`,
            [name, email, passwordHash]
        );

        const user = {
            id: result.insertId,
            name,
            email
        };

        const token = generateToken(user);

        res.status(201).json({
            message: 'Registration successful',
            user,
            token
        });

    } catch (error) {
        next(error);
    }
}

export async function login(req, res, next) {
    try {
        const { email, password } = req.body;

        if (!email || !password) {
            return res.status(400).json({
                error: 'email and password are required'
            });
        }

        const [users] = await pool.execute(
            'SELECT id, name, email, password_hash FROM users WHERE email = ?',
            [email]
        );

        if (users.length === 0) {
            return res.status(401).json({
                error: 'Invalid email or password'
            });
        }

        const user = users[0];

        const passwordMatch = await bcrypt.compare(
            password,
            user.password_hash
        );

        if (!passwordMatch) {
            return res.status(401).json({
                error: 'Invalid email or password'
            });
        }

        const safeUser = {
            id: user.id,
            name: user.name,
            email: user.email
        };

        const token = generateToken(safeUser);

        res.status(200).json({
            message: 'Login successful',
            user: safeUser,
            token
        });

    } catch (error) {
        next(error);
    }
}

export async function getMe(req, res, next) {
    try {
        const [users] = await pool.execute(
            'SELECT id, name, email, created_at, updated_at FROM users WHERE id = ?',
            [req.user.id]
        );

        if (users.length === 0) {
            return res.status(404).json({
                error: 'User not found'
            });
        }

        res.status(200).json({
            user: users[0]
        });

    } catch (error) {
        next(error);
    }
}
