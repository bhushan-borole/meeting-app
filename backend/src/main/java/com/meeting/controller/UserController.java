package com.meeting.controller;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Random;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.meeting.model.Credentials;
import com.meeting.model.User;
import com.meeting.repository.CredentialsRepository;
import com.meeting.repository.UserRepository;


/*All api's related to User in this conroller */
@RestController
@RequestMapping("rest")
public class UserController {
	@Autowired
	UserRepository userRepository;
	@Autowired
	CredentialsRepository credentialsRepository;
	
	
	
	Map<Integer,Integer> map = new HashMap<>();
	
	@PostMapping("/user")
	public User createUser(@RequestBody User user) {
		//go to repo(User) and use save method to insert in DB
		return userRepository.save(user);
	}
	
	
	@GetMapping("/users")
	public List<User> getUsers() {
		//go to repo and fetch all users 
		return userRepository.findAll();
	}
	@GetMapping("/user/{id}")
	public User getUser(@PathVariable("id") int id) {
		//go to repo and fetch user based on id.
		return userRepository.getOne(id);
	}
	
	@PutMapping("/user/{id}")
	public User updateUser(@RequestBody User user,@PathVariable("id") int id) {
		//go to repo and fetch existing user based on id
		User u = userRepository.getOne(id);//existing User
		u.setName(user.getName());
		u.setEmail(user.getEmail());
		//save u in repo
		return userRepository.save(u);
		
	}
	
	@DeleteMapping("/user/{id}")
	public void deleteUser(@PathVariable("id") int id) {
		//go to repo and delete based on id
		userRepository.deleteById(id);
	}
	
	
	@GetMapping("/user/credentials/{userId}")
	public int generateCode(@PathVariable("userId") 
	int userId){
		//go to repo and fetch user based on userId
		User user = userRepository.getOne(userId);
		//send code to email 
		int code = (int)(Math.random() * 100000);
		map.put(userId, code);
		return code;
	}
	
	@GetMapping("/user/verify/{userId}/{code}")
	public boolean verifyCode(@PathVariable("userId") 
	int userId, @PathVariable("code") 
	int code){
		for(Map.Entry<Integer,Integer> e : map.entrySet()){
			if(e.getKey()== userId){
				if(e.getValue()==code){
					map.remove(userId);
					return true;
				}
			}
		}
		return false;
	}
	
	@PostMapping("/user/password/{userId}")
	public User setPassword(@PathVariable("userId") 
	int userId,
	@RequestBody Credentials credentials){
		//go to repo and fetch user info
		User user = userRepository.getOne(userId); //existing
		//save credentials in DB 
		credentials.setUsername(user.getEmail());
		
		Credentials c =credentialsRepository.save(credentials);
		
		//set credentials to User 
		user.setCredentials(c);
		
		//Update the user 
		return userRepository.save(user);
		
	}
}














