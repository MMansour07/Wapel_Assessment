using AutoMapper;
using EMS.Core.Dtos.General;
using EMS.Core.Interfaces;
using EMS.Service.Interfaces;
using System;
using System.Threading.Tasks;
using EMS.Core.Model;
using EMS.Core.Dtos.Rating;
using System.Collections.Generic;
using EMS.Core.Helper;
using System.Data.Entity;

namespace EMS.Service.Services
{
    public class RatingServcie : IRatingServcie
    {
        private readonly IRepository<Rating> _rateRepo;
        private readonly IAuthRepository _authRepository;
        private IMapper _autoMapper;
        public RatingServcie(IMapper autoMapper, IRepository<Rating> rateRepo, IAuthRepository authRepository)
        {
            _autoMapper = autoMapper;
            _rateRepo = rateRepo;
            _authRepository = authRepository;
        }

        public async Task<ResponseModel<NewRatingDto>> CreateRatingAsync(NewRatingDto obj)
        {
            try
            {
                var rate =  await _rateRepo.Add(_autoMapper.Map<NewRatingDto, Rating>(obj));

                return new ResponseModel<NewRatingDto>()
                {
                    Success = true,
                    Data =  _autoMapper.Map<Rating, NewRatingDto>(rate)
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<NewRatingDto>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }

        public async Task<ResponseModel<List<RatingDto>>> GetRatings(string UserId)
        {
            try
            {
                var result = new List<Rating>();

                if (_authRepository.UserInRole(UserId, ERole.HR))
                    result = await _rateRepo.GetAll();

                // to be handeled in case of assiging the manager when creating the users
                else if (_authRepository.UserInRole(UserId, ERole.Manager))
                    result = await _rateRepo.Filter(i => i.Task.User.ManagerId == UserId).ToListAsync();

                // to be handeled in case of assiging the manager when creating the users
                else
                    result = await _rateRepo.Filter(i => i.Task.UserId == UserId).ToListAsync();

                return new ResponseModel<List<RatingDto>>()
                {
                    Success = true,
                    Data = _autoMapper.Map<List<Rating>, List<RatingDto>>(result)
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<List<RatingDto>>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }

        public async Task<ResponseModel<NewRatingDto>> GetRatingInfoAsync(int id)
        {
            try
            {
                var res = await _rateRepo.FindByIdAsync(id);

                return new ResponseModel<NewRatingDto>() { Data = _autoMapper.Map<Rating, NewRatingDto>(res), Success = true };
            }
            catch (Exception ex)
            {
                //logs
                return new ResponseModel<NewRatingDto>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }

    }
}
