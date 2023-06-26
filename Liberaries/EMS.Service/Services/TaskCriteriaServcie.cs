using AutoMapper;
using EMS.Core.Dtos.General;
using EMS.Core.Interfaces;
using EMS.Service.Interfaces;
using System;
using EMS.Core.Dtos.TaskCriteria;
using EMS.Core.Model;
using System.Threading.Tasks;
using System.Collections.Generic;

namespace EMS.Service.Services
{
    public class TaskCriteriaServcie : ITaskCriteriaServcie
    {
        private readonly IRepository<TaskCriteria> _taskCriteria;
        private IMapper _autoMapper;
        public TaskCriteriaServcie(IMapper autoMapper, IRepository<TaskCriteria> taskCriteria)
        {
            _autoMapper = autoMapper;
            _taskCriteria = taskCriteria;
        }

        public async Task<ResponseModel<NewCriteriaDto>> CreateCriteriaAsync(NewCriteriaDto obj)
        {
            try
            {
                var taskCriteria =  await _taskCriteria.Add(_autoMapper.Map<NewCriteriaDto, TaskCriteria>(obj));

                return new ResponseModel<NewCriteriaDto>()
                {
                    Success = true,
                    Data = _autoMapper.Map<TaskCriteria, NewCriteriaDto>(taskCriteria)
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<NewCriteriaDto>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }
        public async Task<ResponseModel<List<CriteriaDto>>> GetCriterias()
        {
            try
            {
                var result = await _taskCriteria.GetAll();

                return new ResponseModel<List<CriteriaDto>>()
                {
                    Success = true,
                    Data = _autoMapper.Map<List<TaskCriteria>, List<CriteriaDto>>(result)
                };
            }
            catch (Exception ex)
            {
                //logs + roll back
                return new ResponseModel<List<CriteriaDto>>() { Ex = ex, Message = ex.Message, Success = false };
            }
        }
    }
}
