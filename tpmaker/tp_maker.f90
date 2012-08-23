SUBROUTINE main(binaryFiles)
      use dimensiones
      use consderper
      use consdernper
      use consderper_f
      use consdernper_f
      use consrs
      use consrs_f
      use funciones 
      use derivvel
      use derivtools
      use velocidades
      use jacobtools
      use mallagrid
      use variables

	integer numFiles
!	character*55 binaryFiles(numFiles)
	character(100) binaryFiles

       integer n1,n2,n3
       integer i,j,k,l

      character(100) outputfield
      character(100) inputfield
      real :: rq,r,macref,mac,pref,spl

      CALL INI ()
      CALL MEMORIA ()
      CALL INIDERIV ()

!      CALL LEERMALLA ()

	numFiles=1

	DO l=1,numFiles
	 outputfield=binaryFiles
!        inputfield='prueba.dat'
         OPEN(11,file=outputfield,form='unformatted')
!        OPEN(61,FILE=inputfield,FORM='formatted')
         READ(11)nd
         READ(11)n1,n2,n3
         READ(11)u
         READ(11)v
         READ(11)w
         READ(11)t
         READ(11)p

!         CALL deriv_VEL()

!         DO i=1,nx
!       	   DO j=1,ny
!       	     DO k=1,nz
!               sum=dvel(i,j,k,4)**2+dvel(i,j,k,7)**2+dvel(i,j,k,2)**2+  &
!               dvel(i,j,k,8)**2+dvel(i,j,k,3)**2+dvel(i,j,k,6)**2
!               sumx=2*(dvel(i,j,k,4)*dvel(i,j,k,2)+dvel(i,j,k,7)*dvel(i,j,k,3)+ &
!               dvel(i,j,k,8)*dvel(i,j,k,6))
!               Rnorm=0.5*(sum-sumx)
!               Snorm=dvel(i,j,k,1)**2+dvel(i,j,k,5)**2+dvel(i,j,k,9)**2+  &
!               0.5*(sum+sumx)
!               q(i,j,k)=0.5*(Rnorm-Snorm)
!               wx(i,j,k)=dvel(i,j,k,8)-dvel(i,j,k,6)
!       	     ENDDO
!       	   ENDDO
!         ENDDO

!       write(61,*)'VARIABLES = "X", "Y", "Z", "U", "V", "W", "P", "T"'
!       write(61,*)'ZONE I=',NX,' J=',NY,' K=',NZ,' DATAPACKING=POINT'
!        DO k=1,nz
!        DO j=1,ny
!        DO i=1,nx
!         r=p(i,j,k)/t(i,j,k)
!         rq=q(i,j,k)
!         if(r.lt.1.)r=1.
!         if(r.gt.2.5)r=2.5
!         if(rq.lt.0.)rq=0.
!         if(rq.gt.25.)rq=25.
!original criterio q         Write(61,100)x(i,j,k),y(i,j,k),z(i,j,k),rq
!         Write(61,100)x(i,j,k),y(i,j,k),z(i,j,k),u(i,j,k),v(i,j,k),w(i,j,k),p(i,j,k),t(i,j,k)
!        enddo
!        enddo
!        enddo
! 100   FORMAT(f16.4,f16.4,f16.4,f16.4,f16.4,f16.4,f16.4,f16.4,f16.4,f16.4)
! 100   FORMAT(f16.6,f16.6,f16.6,f16.6,f16.6,f16.6,f16.6,f16.6,f16.6,f16.6)
        CLOSE(11)
!       CLOSE(61)
       ENDDO
	return
END SUBROUTINE main

      SUBROUTINE ini()
      use dimensiones
      use consfiltro
      use deltas
      nx=150
      ny=109
      nz=109
      cfilt=0.49
      deltax=float(nx-1)
      deltay=float(ny-1)
      deltaz=float(nz-1)
      END SUBROUTINE ini

     SUBROUTINE leermalla()
      use mallagrid
      use dimensiones
      integer n1,n2,n3
      CALL INI()
      allocate(x(nx,ny,nz))
      allocate(y(nx,ny,nz))
      allocate(z(nx,ny,nz))
      open(11,file='tpmaker/jet.grid',form='unformatted')
      read(11)nd
      read(11)n1,n2,n3
      read(11)x
      read(11)y
      read(11)z
      close(11)
     END SUBROUTINE leermalla
