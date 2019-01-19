package com.meeting.controller;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestHeader;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import com.meeting.exception.ResourceNotFoundException;
import com.meeting.model.User;
import com.meeting.repository.CredentialsRepository;
import com.meeting.repository.UserRepository;

@RestController
@RequestMapping("rest")
public class CredentialsController {
	@Autowired
	private CredentialsRepository credentialsRepository;
	@Autowired
	private UserRepository userRepository;
	@GetMapping("/login")
	 @CrossOrigin(origins = {"http://localhost:8080"})
	public User login(@RequestHeader("username") String username,
			@RequestHeader("password") String password){
		User u = userRepository.findByEmail(username);
		if(u != null){
			if(u.getCredentials().getPassword().equals(password)){
				return u;
			}
		}
		throw new ResourceNotFoundException("Credentials Invalid");
		
		
	}
}
