<?php 

namespace App\Models;

use Jenssegers\Mongodb\Eloquent\Model;
use Illuminate\Contracts\Auth\MustVerifyEmail;
use Illuminate\Auth\Authenticatable;
use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Foundation\Auth\User as AuthenticatableUser;
use Illuminate\Notifications\Notifiable;

class User extends Model
{
    protected $connection = 'mongodb';
    protected $collection = 'users';
    protected $fillable = ['name', 'email', 'password'];
}